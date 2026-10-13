-- SQL Server / Azure SQL illustration. Execute only in an approved test DB.
-- This is not part of the portable parameter/file-copy pipeline definitions.
-- Source contract: immutable committed interval (low, high], complete expected count,
-- monotonic version per entity/key, full-row events and explicit delete operations.
CREATE SCHEMA adf_lab;
GO
CREATE TABLE adf_lab.Watermark (
 Entity nvarchar(128) NOT NULL PRIMARY KEY,
 LastVersion bigint NOT NULL
);
CREATE TABLE adf_lab.StageChanges (
 BatchId nvarchar(100) NOT NULL,
 Entity nvarchar(128) NOT NULL,
 OrderId nvarchar(100) NOT NULL,
 ChangeVersion bigint NOT NULL,
 Operation char(1) NOT NULL,
 Amount decimal(18,2) NULL
);
CREATE TABLE adf_lab.OrderState (
 Entity nvarchar(128) NOT NULL,
 OrderId nvarchar(100) NOT NULL,
 ChangeVersion bigint NOT NULL,
 Operation char(1) NOT NULL,
 Amount decimal(18,2) NULL,
 PRIMARY KEY(Entity,OrderId)
);
GO
CREATE OR ALTER PROCEDURE adf_lab.CommitBatch
 @Entity nvarchar(128), @BatchId nvarchar(100),
 @ExpectedLowVersion bigint, @HighVersion bigint, @ExpectedRows bigint
AS
BEGIN
 SET NOCOUNT ON;
 SET XACT_ABORT ON;
 BEGIN TRY
  BEGIN TRANSACTION;
  DECLARE @ActualLow bigint;
  SELECT @ActualLow=LastVersion FROM adf_lab.Watermark WITH (UPDLOCK,HOLDLOCK)
  WHERE Entity=@Entity;
  IF @ActualLow IS NULL OR @ActualLow<>@ExpectedLowVersion OR @HighVersion<@ExpectedLowVersion
   THROW 51001,'Missing/stale/invalid watermark',1;
  IF (SELECT COUNT_BIG(*) FROM adf_lab.StageChanges WHERE Entity=@Entity AND BatchId=@BatchId)<>@ExpectedRows
   THROW 51002,'Incomplete staging count',1;
  IF EXISTS (SELECT 1 FROM adf_lab.StageChanges WHERE Entity=@Entity AND BatchId=@BatchId
   AND (ChangeVersion<=@ExpectedLowVersion OR ChangeVersion>@HighVersion OR Operation NOT IN ('I','U','D')
        OR (Operation<>'D' AND (Amount IS NULL OR Amount<0))))
   THROW 51003,'Invalid source interval or event',1;
  IF EXISTS (
   SELECT OrderId,ChangeVersion FROM adf_lab.StageChanges
   WHERE Entity=@Entity AND BatchId=@BatchId
   GROUP BY OrderId,ChangeVersion
   HAVING COUNT(DISTINCT Operation)>1 OR
    COUNT(DISTINCT CASE WHEN Operation='D' THEN 'DELETE' ELSE CONVERT(varchar(50),Amount) END)>1)
   THROW 51004,'Conflicting key/version payload',1;
  ;WITH Ranked AS (
   SELECT Entity,OrderId,ChangeVersion,Operation,
          CASE WHEN Operation='D' THEN NULL ELSE Amount END AS Amount,
          ROW_NUMBER() OVER(PARTITION BY Entity,OrderId ORDER BY ChangeVersion DESC) AS rn
   FROM adf_lab.StageChanges WHERE Entity=@Entity AND BatchId=@BatchId
  )
  MERGE adf_lab.OrderState WITH (HOLDLOCK) AS t
  USING (SELECT Entity,OrderId,ChangeVersion,Operation,Amount FROM Ranked WHERE rn=1) AS s
  ON t.Entity=s.Entity AND t.OrderId=s.OrderId
  WHEN MATCHED AND s.ChangeVersion>t.ChangeVersion THEN
   UPDATE SET ChangeVersion=s.ChangeVersion,Operation=s.Operation,Amount=s.Amount
  WHEN NOT MATCHED THEN INSERT(Entity,OrderId,ChangeVersion,Operation,Amount)
   VALUES(s.Entity,s.OrderId,s.ChangeVersion,s.Operation,s.Amount);
  UPDATE adf_lab.Watermark SET LastVersion=@HighVersion WHERE Entity=@Entity;
  COMMIT;
 END TRY
 BEGIN CATCH
  IF XACT_STATE()<>0 ROLLBACK;
  THROW;
 END CATCH
END;
GO
CREATE VIEW adf_lab.CurrentOrders AS
 SELECT Entity,OrderId,ChangeVersion,Amount FROM adf_lab.OrderState WHERE Operation<>'D';
GO
-- Add source expected-count/snapshot proof, schema/contract checks, retained-state
-- conflict auditing, accepted batch ledger and idempotent response for replay.
-- A repeated request after successful commit currently rejects its stale low
-- boundary; the orchestrator must inspect accepted state, not append again.
-- Test actual SQL semantics/concurrency, MERGE/locking performance and permissions
-- before using this illustration in production. It has not been SQL-executed here.
