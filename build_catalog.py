from pathlib import Path
import json, sqlite3, textwrap
ROOT = Path(__file__).resolve().parent
QUESTIONS = []
SOURCES = {
 'pairs': ('HackerRank Symmetric Pairs', 'https://www.hackerrank.com/challenges/symmetric-pairs/problem'),
 'projects': ('HackerRank SQL Project Planning', 'https://www.hackerrank.com/challenges/sql-projects/problem'),
 'stadium': ('LeetCode Human Traffic of Stadium', 'https://leetcode.com/problems/human-traffic-of-stadium/'),
 'allproducts': ('LeetCode Customers Who Bought All Products', 'https://leetcode.com/problems/customers-who-bought-all-products/'),
 'friends': ('LeetCode Friend Requests II', 'https://leetcode.com/problems/friend-requests-ii-who-has-the-most-friends/'),
 'tree': ('LeetCode Tree Node', 'https://leetcode.com/problems/tree-node/'),
 'seats': ('LeetCode Exchange Seats', 'https://leetcode.com/problems/exchange-seats/'),
 'price': ('LeetCode Product Price at a Given Date', 'https://leetcode.com/problems/product-price-at-a-given-date/'),
 'restaurant': ('LeetCode Restaurant Growth', 'https://leetcode.com/problems/restaurant-growth/'),
 'bus': ('LeetCode Last Person to Fit in the Bus', 'https://leetcode.com/problems/last-person-to-fit-in-the-bus/'),
 'consecutive': ('LeetCode Consecutive Numbers', 'https://leetcode.com/problems/consecutive-numbers/'),
 'insurance': ('LeetCode Investments in 2016', 'https://leetcode.com/problems/investments-in-2016/'),
 'sessions': ('Ryan Guill Aggregating event data into sessions', 'https://ryanguill.com/postgresql/sql/2024/06/24/aggregating-event-data-into-sessions.html'),
 'supply': ('Itzik Ben Gan Matching Supply With Demand Challenge', 'https://sqlperformance.com/2021/12/t-sql-queries/supply-demand-challenge'),
 'supplysolution': ('Itzik Ben Gan Matching Supply With Demand Solutions Part 1', 'https://sqlperformance.com/2022/01/t-sql-queries/supply-demand-solutions-1'),
 'fifo': ('Kathi Kellenberger FIFO Stock Inventory', 'https://www.red-gate.com/simple-talk/databases/sql-server/performance-sql-server/set-based-speed-phreakery-the-fifo-stock-inventory-sql-problem/'),
 'intervals': ('C R Timmons SQL Packing Intervals', 'https://www.crtimmonsinc.com/2018/05/04/packing-intervals/'),
 'closest': ('Itzik Ben Gan Closest Match Part 1', 'https://sqlperformance.com/2018/12/t-sql-queries/closest-match-part-1'),
 'window': ('SQLite Window Functions', 'https://sqlite.org/windowfunctions.html'),
 'recursive': ('SQLite WITH and recursive graph queries', 'https://www.sqlite.org/lang_with.html'),
 'expr': ('SQLite SQL Expressions', 'https://www.sqlite.org/lang_expr.html'),
 'select': ('SQLite SELECT and joins', 'https://www.sqlite.org/lang_select.html'),
 'pgwindow': ('PostgreSQL Window Functions', 'https://www.postgresql.org/docs/current/functions-window.html'),
 'pgsubquery': ('PostgreSQL Subquery Expressions', 'https://www.postgresql.org/docs/current/functions-subquery.html'),
 'pgjoin': ('PostgreSQL Table Expressions', 'https://www.postgresql.org/docs/current/queries-table-expressions.html'),
 'pgrecursive': ('PostgreSQL Recursive Queries', 'https://www.postgresql.org/docs/current/queries-with.html'),
}
def table(name, columns, rows):
    return {'name': name, 'columns': [c.split(':', 1) for c in columns.split(',')], 'rows': rows}
def add(title, pattern, difficulty, source, origin, prompt, tables, sql, expected, explanation, trap, followup, alternatives=None):
    QUESTIONS.append(dict(id=f'Q{len(QUESTIONS)+1:02}', title=title, pattern=pattern, difficulty=difficulty,
        source=source, origin=origin, prompt=prompt, tables=tables, sql=textwrap.dedent(sql).strip(), expected=expected,
        explanation=explanation, trap=trap, followup=followup, alternatives=alternatives or []))

t = table
add('Deduplicate reverse routes while preserving an original row', 'Unordered pairs and symmetry breaking', 'Medium', 'pairs', 'Original extension of a symmetric pair pattern',
    'Treat (source, destination, distance) and its reversal as one route. Preserve the smallest row_id in each duplicate group, including exact duplicates. Different distances are different routes; keep self routes and lone reverse-oriented routes. Endpoints and distance are non-null.',
    [t('routes','row_id:INTEGER PRIMARY KEY,src:TEXT,dst:TEXT,dist:INTEGER',[(1,'A','B',10),(2,'B','A',10),(3,'A','C',5),(4,'D','C',7),(5,'A','B',10),(6,'A','A',0),(7,'B','A',12)])],
    '''WITH canonical AS (
      SELECT *, CASE WHEN src <= dst THEN src ELSE dst END AS lo,
                CASE WHEN src <= dst THEN dst ELSE src END AS hi
      FROM routes
    ), keep AS (
      SELECT MIN(row_id) AS row_id FROM canonical GROUP BY lo, hi, dist
    )
    SELECT r.row_id, r.src, r.dst, r.dist
    FROM routes r JOIN keep k ON r.row_id = k.row_id
    ORDER BY r.row_id;''',
    [(1,'A','B',10),(3,'A','C',5),(4,'D','C',7),(6,'A','A',0),(7,'B','A',12)],
    'Canonical endpoints define the duplicate key, but joining retained IDs back to the source preserves original direction. The distance belongs to the key because the prompt says different distances are distinct.',
    'WHERE src < dst loses the lone D to C route and every self route. DISTINCT on the original columns does not normalize direction.',
    'If distance is excluded from the key, which conflicting distance should survive?',
    [('LEFT self anti join', '''SELECT a.row_id, a.src, a.dst, a.dist
    FROM routes a
    LEFT JOIN routes b
      ON b.row_id < a.row_id AND b.dist = a.dist
     AND ((b.src = a.src AND b.dst = a.dst)
       OR (b.src = a.dst AND b.dst = a.src))
    WHERE b.row_id IS NULL
    ORDER BY a.row_id;''')])
add('Find reciprocal pairs without matching a row to itself', 'Unordered pairs and symmetry breaking', 'Medium', 'pairs', 'Adapted practice problem with fresh data',
    'Return (x,y) with x <= y when two distinct input rows establish both directions. A self pair (x,x) needs at least two physical rows. Return each pair once.',
    [t('pairs','id:INTEGER PRIMARY KEY,x:INTEGER,y:INTEGER',[(1,1,2),(2,2,1),(3,3,3),(4,4,4),(5,4,4),(6,5,6),(7,1,2)])],
    '''SELECT DISTINCT a.x, a.y
    FROM pairs a JOIN pairs b
      ON a.x = b.y AND a.y = b.x AND a.id <> b.id
    WHERE a.x <= a.y
    ORDER BY a.x, a.y;''', [(1,2),(4,4)],
    'The ID inequality forces a different physical row. The endpoint inequality picks one orientation; DISTINCT handles repeated witnesses.',
    'A self join on endpoints alone incorrectly certifies the single (3,3) row as reciprocal.',
    'Without a row ID, how would grouping and counts distinguish one self pair from two?')
add('Count undirected neighbors despite duplicated edge directions', 'Graph edge normalization', 'Medium', 'friends', 'Original extension of a published bidirectional friendship problem',
    'Return each registered person and the number of distinct other people connected to them. Edges are undirected; duplicate directions and self edges must not inflate counts. Include isolated people.',
    [t('people','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,),(4,)]),t('edges','a:INTEGER,b:INTEGER',[(1,2),(2,1),(1,2),(2,3),(3,3)])],
    '''WITH directed AS (
      SELECT a AS person, b AS neighbor FROM edges WHERE a <> b
      UNION
      SELECT b, a FROM edges WHERE a <> b
    )
    SELECT p.id, COUNT(d.neighbor) AS neighbors
    FROM people p LEFT JOIN directed d ON d.person = p.id
    GROUP BY p.id ORDER BY p.id;''', [(1,1),(2,2),(3,1),(4,0)],
    'UNION constructs a set of directed neighbor relationships. The master people table retains isolated vertices.',
    'UNION ALL counts duplicate edges. COUNT(*) gives an isolated person a count of one after a LEFT JOIN.',
    'How would you return actual mutual friends between two people instead of degrees?')
add('Find graph triangles exactly once', 'Graph edge normalization', 'Hard', 'recursive', 'Original practice extension',
    'Return all undirected triangles as a < b < c. Ignore duplicate edges and self edges. A triangle requires all three edges, not just a two-hop path.',
    [t('edges','src:INTEGER,dst:INTEGER',[(1,2),(2,1),(2,3),(1,3),(1,4),(3,4),(4,4)])],
    '''WITH e AS (
      SELECT DISTINCT CASE WHEN src < dst THEN src ELSE dst END AS a,
                      CASE WHEN src < dst THEN dst ELSE src END AS b
      FROM edges WHERE src <> dst
    )
    SELECT x.a, x.b, y.b AS c
    FROM e x JOIN e y ON x.b = y.a
    JOIN e z ON z.a = x.a AND z.b = y.b
    ORDER BY x.a, x.b, y.b;''', [(1,2,3),(1,3,4)],
    'Canonical edges enforce a strict vertex order. Two joined edges form a path; the third join closes it.',
    'Three unrestricted self joins return permutations of the same triangle. A two-edge path is not a triangle.',
    'How would directed cycles differ from undirected triangles?')
add('Assign connected components including isolated nodes', 'Recursive reachability', 'Hard', 'recursive', 'Original practice extension',
    'Return each node with the smallest node ID in its undirected connected component. Include isolated nodes. Edges can contain cycles and duplicates.',
    [t('nodes','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,),(4,),(5,),(6,)]),t('edges','a:INTEGER,b:INTEGER',[(1,2),(2,3),(3,1),(4,5),(1,2)])],
    '''WITH RECURSIVE e(a,b) AS (
      SELECT a,b FROM edges UNION SELECT b,a FROM edges
    ), reach(root,node) AS (
      SELECT id,id FROM nodes
      UNION
      SELECT r.root,e.b FROM reach r JOIN e ON e.a=r.node
    )
    SELECT node, MIN(root) AS component
    FROM reach GROUP BY node ORDER BY node;''', [(1,1),(2,1),(3,1),(4,4),(5,4),(6,6)],
    'Start from every node and expand reachability. UNION deduplicates the complete (root,node) state, allowing finite termination on cycles.',
    'UNION ALL loops on cycles. Adding an ever-increasing depth to the deduplication state would defeat cycle termination.',
    'What changes if you need shortest paths instead of reachability?')
add('Compress integer sequences with duplicate input values', 'Gaps and islands', 'Medium', 'projects', 'Original practice extension of contiguous grouping',
    'Return start_value, end_value, and distinct length for every maximal consecutive integer run. Duplicate observations count once.',
    [t('observations','value:INTEGER',[(1,),(2,),(2,),(3,),(7,),(8,),(10,)])],
    '''WITH d AS (SELECT DISTINCT value FROM observations),
    g AS (SELECT value, value-ROW_NUMBER() OVER (ORDER BY value) AS island FROM d)
    SELECT MIN(value) AS start_value, MAX(value) AS end_value, COUNT(*) AS length
    FROM g GROUP BY island ORDER BY start_value;''', [(1,3,3),(7,8,2),(10,10,1)],
    'After deduplication, value and row number increase together inside a run, so their difference is constant.',
    'Numbering duplicate values first splits a legitimate run. Grouping by value alone does not identify adjacency.',
    'How would you change the break condition if a gap of two were allowed?')
add('Find every longest login streak with duplicate logins', 'Gaps and islands', 'Medium', 'projects', 'Original practice extension',
    'day_no is a calendar-day ordinal, not a YYYYMMDD integer. Return all longest streaks per user, including ties. Multiple logins on the same day count once.',
    [t('logins','user_id:INTEGER,day_no:INTEGER',[(1,1),(1,2),(1,2),(1,4),(1,5),(2,2),(2,3),(2,4)])],
    '''WITH d AS (SELECT DISTINCT user_id,day_no FROM logins),
    g AS (
      SELECT *,day_no-ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day_no) AS island FROM d
    ), streaks AS (
      SELECT user_id,MIN(day_no) AS start_day,MAX(day_no) AS end_day,COUNT(*) AS days
      FROM g GROUP BY user_id,island
    ), ranked AS (
      SELECT *,MAX(days) OVER (PARTITION BY user_id) AS longest FROM streaks
    )
    SELECT user_id,start_day,end_day,days FROM ranked
    WHERE days=longest ORDER BY user_id,start_day;''', [(1,1,2,2),(1,4,5,2),(2,2,4,3)],
    'First build streaks, then compare their lengths within each user. Comparing against the maximum keeps both equally long streaks.',
    'ROW_NUMBER() = 1 over streak length arbitrarily discards ties. YYYYMMDD subtraction is not calendar arithmetic.',
    'For actual DATE columns, what date arithmetic does your SQL dialect require?')
add('Find missing ranges including the boundaries', 'Gaps and islands', 'Medium', 'recursive', 'Original practice extension',
    'Find all missing inclusive integer ranges within 1 through 12. Existing IDs are distinct and within the bounds. Include leading and trailing gaps without returning each missing ID separately.',
    [t('ids','id:INTEGER PRIMARY KEY',[(3,),(4,),(8,),(10,)])],
    '''WITH points AS (
      SELECT 0 AS id UNION SELECT id FROM ids UNION SELECT 13
    ), n AS (SELECT id,LEAD(id) OVER (ORDER BY id) AS next_id FROM points)
    SELECT id+1 AS gap_start,next_id-1 AS gap_end
    FROM n WHERE next_id > id+1 ORDER BY gap_start;''', [(1,2),(5,7),(9,9),(11,12)],
    'Sentinels just outside the allowed range expose both boundary gaps. LEAD gives each neighboring pair of observed points.',
    'Looking only between existing rows misses the beginning and end. Expanding every absent number can be expensive for large ranges.',
    'What should happen when the input is empty? The answer should be the entire allowed range.')
add('Sessionize events with an exact inactivity threshold', 'Sessionization and change points', 'Medium', 'sessions', 'Adapted pattern with fresh data and explicit boundary semantics',
    'minute_no is an elapsed-minute ordinal. Start a new session only when the gap from the previous event is greater than 30 minutes. Equal timestamps are ordered by event_id. Return user, session number, start minute, end minute, and event count.',
    [t('events','event_id:INTEGER PRIMARY KEY,user_id:INTEGER,minute_no:INTEGER',[(1,1,0),(2,1,30),(3,1,61),(4,1,61),(5,2,5),(6,2,40)])],
    '''WITH p AS (
      SELECT *,LAG(minute_no) OVER (PARTITION BY user_id ORDER BY minute_no,event_id) AS prev FROM events
    ), f AS (
      SELECT *,CASE WHEN prev IS NULL OR minute_no-prev>30 THEN 1 ELSE 0 END AS fresh FROM p
    ), g AS (
      SELECT *,SUM(fresh) OVER (PARTITION BY user_id ORDER BY minute_no,event_id ROWS UNBOUNDED PRECEDING) AS session_no FROM f
    )
    SELECT user_id,session_no,MIN(minute_no) AS start_minute,MAX(minute_no) AS end_minute,COUNT(*) AS events
    FROM g GROUP BY user_id,session_no ORDER BY user_id,session_no;''', [(1,1,0,30,2),(1,2,61,61,2),(2,1,5,5,1),(2,2,40,40,1)],
    'LAG measures inactivity between adjacent events; a running sum of break flags labels sessions.',
    'Using >= 30 changes the exact boundary. Bucketing by minute_no / 30 ignores activity chains that cross fixed bucket boundaries.',
    'Should late-arriving events be allowed to merge two sessions that were already published?')
add('Group status runs with NULL states and missing days', 'Sessionization and change points', 'Hard', 'window', 'Original practice extension',
    'Return maximal runs of the same status on consecutive calendar-day ordinals. NULL is a legitimate status and equals another NULL for grouping. A missing day breaks a run even if status stays the same. One row exists per day.',
    [t('daily','day_no:INTEGER PRIMARY KEY,status:TEXT',[(1,'up'),(2,'up'),(3,None),(4,None),(6,None),(7,'up')])],
    '''WITH p AS (
      SELECT *,LAG(day_no) OVER (ORDER BY day_no) AS prev_day,
               LAG(status) OVER (ORDER BY day_no) AS prev_status FROM daily
    ), f AS (
      SELECT *,CASE WHEN day_no=prev_day+1 AND
        (status=prev_status OR (status IS NULL AND prev_status IS NULL))
        THEN 0 ELSE 1 END AS fresh FROM p
    ), g AS (
      SELECT *,SUM(fresh) OVER (ORDER BY day_no ROWS UNBOUNDED PRECEDING) AS island FROM f
    )
    SELECT status,MIN(day_no) AS start_day,MAX(day_no) AS end_day
    FROM g GROUP BY island,status ORDER BY start_day;''', [('up',1,2),(None,3,4),(None,6,6),('up',7,7)],
    'A boundary depends on both calendar adjacency and null-aware state equality. Explicitly handling NULL preserves the intended unknown-state run.',
    'status <> LAG(status) evaluates to unknown around NULLs. Grouping only by status merges separated runs.',
    'How should conflicting status observations for the same day be resolved?')
add('Return every row in qualifying ID streaks', 'Gaps and islands', 'Medium', 'stadium', 'Adapted problem with fresh data',
    'Return all rows belonging to at least three consecutive IDs whose attendance is at least 100. Adjacency is by ID, not by calendar date. IDs are unique.',
    [t('visits','id:INTEGER PRIMARY KEY,day_no:INTEGER,people:INTEGER',[(1,1,90),(2,2,110),(3,3,120),(4,4,90),(5,5,130),(6,6,140),(7,9,150),(9,10,160)])],
    '''WITH g AS (
      SELECT *,id-ROW_NUMBER() OVER (ORDER BY id) AS island
      FROM visits WHERE people>=100
    ), c AS (SELECT *,COUNT(*) OVER (PARTITION BY island) AS run_length FROM g)
    SELECT id,day_no,people FROM c WHERE run_length>=3 ORDER BY id;''', [(5,5,130),(6,6,140),(7,9,150)],
    'Filter qualifying observations before deriving ID islands. A window count labels every row with its island size.',
    'Calendar-date gaps are irrelevant here. Returning only each island boundary omits required interior rows.',
    'What changes when the interviewer asks for consecutive dates instead of IDs?')
add('Reconstruct projects from one-day tasks', 'Gaps and islands', 'Medium', 'projects', 'Adapted problem with fresh data',
    'Each task covers [start_day,end_day) and lasts exactly one day. Tasks do not overlap. Adjacent tasks belong to one project. Return project start, end, and duration, ordered by duration then start.',
    [t('tasks','id:INTEGER PRIMARY KEY,start_day:INTEGER,end_day:INTEGER',[(1,1,2),(2,2,3),(3,5,6),(4,8,9),(5,9,10),(6,10,11)])],
    '''WITH g AS (
      SELECT *,start_day-ROW_NUMBER() OVER (ORDER BY start_day) AS island FROM tasks
    )
    SELECT MIN(start_day) AS project_start,MAX(end_day) AS project_end,
           MAX(end_day)-MIN(start_day) AS duration
    FROM g GROUP BY island ORDER BY duration,project_start;''', [(5,6,1),(1,3,2),(8,11,3)],
    'The one-day, non-overlapping contract turns project reconstruction into integer islands on task starts.',
    'This arithmetic shortcut fails when tasks have variable durations or overlap; interval packing is then required.',
    'Would touching tasks still form a project if end boundaries were inclusive?')
add('Merge overlapping intervals even when they are nested', 'Interval packing and sweep lines', 'Hard', 'intervals', 'Adapted pattern with a nested-interval counterexample',
    'Merge intervals into maximal coverage ranges. Intervals use [start,end); touching intervals merge. Input intervals have positive lengths and unique IDs. Include nested ranges correctly.',
    [t('intervals','id:INTEGER PRIMARY KEY,start_at:INTEGER,end_at:INTEGER',[(1,1,10),(2,2,3),(3,4,8),(4,10,12),(5,15,17)])],
    '''WITH p AS (
      SELECT *,MAX(end_at) OVER (ORDER BY start_at,end_at,id
        ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS previous_max
      FROM intervals
    ), f AS (
      SELECT *,CASE WHEN previous_max IS NULL OR start_at>previous_max THEN 1 ELSE 0 END AS fresh FROM p
    ), g AS (
      SELECT *,SUM(fresh) OVER (ORDER BY start_at,end_at,id ROWS UNBOUNDED PRECEDING) AS island FROM f
    )
    SELECT MIN(start_at) AS start_at,MAX(end_at) AS end_at
    FROM g GROUP BY island ORDER BY start_at;''', [(1,12),(15,17)],
    'Compare each start with the largest prior end, not merely the previous row end. That prior envelope remembers long intervals even after short nested ones.',
    'LAG(end_at) sees 3 before the interval starting at 4 and incorrectly splits coverage still protected by [1,10).',
    'Change > to >= if touching intervals should remain separate. Partition all windows when intervals belong to different resources.')
add('Find free time between overlapping bookings', 'Interval packing and sweep lines', 'Hard', 'intervals', 'Original practice extension',
    'Within [0,20), return every maximal free interval. Bookings are positive-length half-open intervals fully inside the requested window. Touching occupied intervals leave no gap.',
    [t('bookings','id:INTEGER PRIMARY KEY,start_at:INTEGER,end_at:INTEGER',[(1,1,5),(2,3,7),(3,10,12),(4,12,16)])],
    '''WITH p AS (
      SELECT *,MAX(end_at) OVER (ORDER BY start_at,end_at,id
        ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS mx FROM bookings
    ), f AS (
      SELECT *,CASE WHEN mx IS NULL OR start_at>mx THEN 1 ELSE 0 END AS fresh FROM p
    ), g AS (
      SELECT *,SUM(fresh) OVER (ORDER BY start_at,end_at,id ROWS UNBOUNDED PRECEDING) AS grp FROM f
    ), packed AS (
      SELECT MIN(start_at) AS s,MAX(end_at) AS e FROM g GROUP BY grp
    ), padded AS (
      SELECT s,e FROM packed UNION ALL SELECT 0,0 UNION ALL SELECT 20,20
    ), gaps AS (
      SELECT e AS free_start,LEAD(s) OVER (ORDER BY s,e) AS free_end FROM padded
    )
    SELECT free_start,free_end FROM gaps WHERE free_end>free_start ORDER BY free_start;''', [(0,1),(7,10),(16,20)],
    'Pack occupied coverage before taking its complement. Boundary sentinels expose free time before the first booking and after the last.',
    'Taking LEAD directly over raw bookings invents free intervals inside overlapping bookings.',
    'How would you clip bookings that start before 0 or end after 20?')
add('Find peak simultaneous meetings with tied event times', 'Interval packing and sweep lines', 'Hard', 'window', 'Original practice exercise',
    'Meetings are half-open intervals: a meeting ending at time t is inactive at t. Return every positive-duration segment having the maximum simultaneous meeting count.',
    [t('meetings','id:INTEGER PRIMARY KEY,start_at:INTEGER,end_at:INTEGER',[(1,1,4),(2,2,5),(3,4,6),(4,4,7)])],
    '''WITH events AS (
      SELECT start_at AS at,1 AS delta FROM meetings
      UNION ALL SELECT end_at,-1 FROM meetings
    ), grouped AS (SELECT at,SUM(delta) AS delta FROM events GROUP BY at),
    swept AS (
      SELECT at,LEAD(at) OVER (ORDER BY at) AS until,
             SUM(delta) OVER (ORDER BY at ROWS UNBOUNDED PRECEDING) AS active
      FROM grouped
    ), segments AS (SELECT * FROM swept WHERE until>at),
    peaks AS (SELECT *,MAX(active) OVER () AS peak FROM segments)
    SELECT at AS start_at,until AS end_at,active FROM peaks WHERE active=peak ORDER BY at;''', [(4,5,3)],
    'Collapse simultaneous starts and ends into one net change. The running active count applies to the interval from that time to the next event.',
    'Processing starts before ends can create a fake zero-duration peak. Counting overlapping pairs is not a concurrency measure.',
    'If meetings use closed intervals, what must change at equal endpoints?')
add('Measure occupied duration without counting overlaps twice', 'Interval packing and sweep lines', 'Hard', 'intervals', 'Original practice extension',
    'Return total occupied duration across half-open intervals. Duplicate and nested coverage must count once. Touching ranges may be merged.',
    [t('ranges','id:INTEGER PRIMARY KEY,s:INTEGER,e:INTEGER',[(1,1,10),(2,2,3),(3,9,12),(4,15,18)])],
    '''WITH p AS (
      SELECT *,MAX(e) OVER (ORDER BY s,e,id ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS mx FROM ranges
    ), f AS (SELECT *,CASE WHEN mx IS NULL OR s>mx THEN 1 ELSE 0 END AS fresh FROM p),
    g AS (SELECT *,SUM(fresh) OVER (ORDER BY s,e,id ROWS UNBOUNDED PRECEDING) AS grp FROM f),
    packed AS (SELECT MIN(s) AS s,MAX(e) AS e FROM g GROUP BY grp)
    SELECT COALESCE(SUM(e-s),0) AS occupied FROM packed;''', [(14,)],
    'Pack the union of coverage, then measure the disjoint ranges. COALESCE gives zero when there are no intervals.',
    'SUM(end-start) measures total booked effort, not unique occupied time.',
    'Can you compute the same measure from sweep-line segments where active > 0?')
add('Resolve prices as of a date while keeping products without history', 'Temporal and nearest joins', 'Medium', 'price', 'Adapted pattern with fresh data and a product master',
    'Return every product price at day_no 5. Use the most recent change at or before that day; otherwise use default price 10. Product IDs come from a master table, so products with no history must appear. Changes are unique by product and day.',
    [t('products','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,),(4,)]),t('changes','product_id:INTEGER,day_no:INTEGER,price:INTEGER',[(1,2,20),(1,5,30),(1,8,99),(2,7,40),(3,3,15)])],
    '''WITH eligible AS (
      SELECT *,ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY day_no DESC) AS rn
      FROM changes WHERE day_no<=5
    )
    SELECT p.id,COALESCE(e.price,10) AS price
    FROM products p LEFT JOIN eligible e ON e.product_id=p.id AND e.rn=1
    ORDER BY p.id;''', [(1,30),(2,10),(3,15),(4,10)],
    'Restrict history to the as-of boundary before choosing a row. Driving from the master preserves future-only and history-free products. Stored prices are non-null.',
    'Ranking all history first and then filtering the newest row by date can erase the valid earlier price.',
    'If a stored price can be NULL, why must you test row existence rather than COALESCE(price,10)?')
add('Join facts to effective-dated dimensions at a shared boundary', 'Temporal and nearest joins', 'Medium', 'pgjoin', 'Original practice exercise',
    'Attach the effective label to each fact using [valid_from,valid_to). NULL valid_to means open-ended. Return NULL for uncovered facts. Dimension periods for each key never overlap.',
    [t('facts','id:INTEGER PRIMARY KEY,key_id:INTEGER,at:INTEGER',[(1,1,4),(2,1,5),(3,1,10),(4,2,5)]),t('versions','key_id:INTEGER,valid_from:INTEGER,valid_to:INTEGER,label:TEXT',[(1,1,5,'old'),(1,5,10,'new'),(1,10,None,'latest')])],
    '''SELECT f.id,v.label
    FROM facts f LEFT JOIN versions v
      ON v.key_id=f.key_id AND f.at>=v.valid_from
     AND (f.at<v.valid_to OR v.valid_to IS NULL)
    ORDER BY f.id;''', [(1,'old'),(2,'new'),(3,'latest'),(4,None)],
    'The lower bound is inclusive and the upper bound exclusive. Put eligibility in ON so uncovered facts survive.',
    'BETWEEN includes both ends and matches the fact at 5 to two versions.',
    'How would you detect overlapping dimension periods before trusting this join?')
add('Choose the closest observation with a deterministic tie rule', 'Temporal and nearest joins', 'Hard', 'closest', 'Adapted pattern with fresh data',
    'For each target minute, choose the nearest reading. A distance tie prefers the earlier reading minute, then the smaller reading ID. There is at least one reading; reading timestamps may duplicate.',
    [t('targets','id:INTEGER PRIMARY KEY,at:INTEGER',[(1,5),(2,10),(3,0)]),t('readings','id:INTEGER PRIMARY KEY,at:INTEGER,value:INTEGER',[(1,3,30),(2,7,70),(3,7,71),(4,12,120)])],
    '''WITH candidates AS (
      SELECT t.id AS target_id,r.id AS reading_id,r.at,r.value,
        ROW_NUMBER() OVER (PARTITION BY t.id ORDER BY ABS(t.at-r.at),r.at,r.id) AS rn
      FROM targets t CROSS JOIN readings r
    )
    SELECT target_id,reading_id,value FROM candidates WHERE rn=1 ORDER BY target_id;''', [(1,1,30),(2,4,120),(3,1,30)],
    'The ordering expresses all tie-breakers. This exhaustive candidate version favors clarity for small examples, not production-scale efficiency.',
    'MIN(ABS(...)) alone can return multiple tied candidates. Ordering by distance alone leaves the winner unspecified.',
    'At scale, how could predecessor and successor seeks avoid a full cross join?')
add('Find nonbuyers when the purchase table contains NULL', 'NULL semantics and anti joins', 'Medium', 'pgsubquery', 'Original semantics exercise',
    'Return registered customer IDs with no matching purchase. A purchase can have an unknown customer_id represented by NULL; it does not match any registered customer.',
    [t('customers','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,)]),t('purchases','id:INTEGER PRIMARY KEY,customer_id:INTEGER',[(1,1),(2,None)])],
    '''SELECT c.id FROM customers c
    WHERE NOT EXISTS (SELECT 1 FROM purchases p WHERE p.customer_id=c.id)
    ORDER BY c.id;''', [(2,),(3,)],
    'NOT EXISTS asks whether a matching row exists, so the unrelated NULL key cannot poison the result.',
    'id NOT IN (SELECT customer_id FROM purchases) yields unknown for nonmatching IDs when the subquery contains NULL.',
    'How would you implement the same anti join with LEFT JOIN and a non-nullable purchase ID?',
    [('LEFT anti join', '''SELECT c.id FROM customers c
    LEFT JOIN purchases p ON p.customer_id=c.id
    WHERE p.id IS NULL ORDER BY c.id;''')])
add('Keep parents that have no qualifying child rows', 'NULL semantics and anti joins', 'Medium', 'pgjoin', 'Original semantics exercise',
    'Return every customer with the number of paid orders. Customers with only cancelled orders, or no orders, must have zero.',
    [t('customers','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,)]),t('orders','id:INTEGER PRIMARY KEY,customer_id:INTEGER,status:TEXT',[(11,1,'paid'),(12,1,'cancelled'),(13,2,'cancelled')])],
    '''SELECT c.id,COUNT(o.id) AS paid_orders
    FROM customers c LEFT JOIN orders o
      ON o.customer_id=c.id AND o.status='paid'
    GROUP BY c.id ORDER BY c.id;''', [(1,1),(2,0),(3,0)],
    'Apply the child eligibility predicate in ON. Count the child key, not the null-extended parent row.',
    "WHERE o.status='paid' after the LEFT JOIN eliminates customers 2 and 3. WHERE status='paid' OR status IS NULL still loses customer 2.",
    'Why does the OR status IS NULL workaround fail when nonqualifying child rows exist?')
add('Aggregate orders and payments without join fan out', 'Join grain and multiplicity', 'Hard', 'pgjoin', 'Original practice exercise',
    'Return every customer, total order amount, and total payment amount. Orders and payments are separate one-to-many children of customers. A customer can have no child rows. Amounts are non-null.',
    [t('customers','id:INTEGER PRIMARY KEY',[(1,),(2,)]),t('orders','id:INTEGER PRIMARY KEY,customer_id:INTEGER,amount:INTEGER',[(1,1,50),(2,1,50)]),t('payments','id:INTEGER PRIMARY KEY,customer_id:INTEGER,amount:INTEGER',[(1,1,30),(2,1,30),(3,1,40)])],
    '''WITH o AS (SELECT customer_id,SUM(amount) AS total FROM orders GROUP BY customer_id),
    p AS (SELECT customer_id,SUM(amount) AS total FROM payments GROUP BY customer_id)
    SELECT c.id,COALESCE(o.total,0) AS ordered,COALESCE(p.total,0) AS paid
    FROM customers c LEFT JOIN o ON o.customer_id=c.id
    LEFT JOIN p ON p.customer_id=c.id ORDER BY c.id;''', [(1,100,100),(2,0,0)],
    'Reduce each child independently to one row per customer before joining. This makes both measures live at the same grain.',
    'The raw join creates 2 x 3 rows for customer 1. SUM(DISTINCT amount) undercounts legitimate equal-value orders and payments.',
    'How would you add refunds as a third independent child without multiplying rows?')
add('Preserve independent transaction amounts when duplicate values are valid', 'Join grain and multiplicity', 'Medium', 'select', 'Original practice exercise',
    'Sum the amount of invoices having at least one approved tag. Each invoice contributes once, even if multiple approved tags exist. Equal amounts on different invoices are legitimate.',
    [t('invoices','id:INTEGER PRIMARY KEY,amount:INTEGER',[(1,50),(2,50),(3,100)]),t('tags','invoice_id:INTEGER,tag:TEXT',[(1,'approved'),(1,'approved'),(2,'approved'),(3,'draft')])],
    '''SELECT COALESCE(SUM(i.amount),0) AS approved_total
    FROM invoices i WHERE EXISTS (
      SELECT 1 FROM tags t WHERE t.invoice_id=i.id AND t.tag='approved'
    );''', [(100,)],
    'EXISTS tests eligibility without expanding invoice rows. The sum therefore counts invoice identities rather than distinct numeric values.',
    'SUM after a raw join returns 150; SUM(DISTINCT amount) returns 50. Both are wrong for opposite reasons.',
    'How would you return qualifying invoice detail without relying on DISTINCT?')
add('Reconcile two snapshots including NULL-valued changes', 'Set and multiset reconciliation', 'Hard', 'expr', 'Original practice exercise',
    'Both snapshots have a unique non-null ID. Return added, removed, or changed IDs. NULL to value and value to NULL are changes; NULL to NULL is unchanged. Output id, change_kind, old_value, new_value.',
    [t('old_snapshot','id:INTEGER PRIMARY KEY,val:TEXT',[(1,'a'),(2,None),(3,'c'),(5,None)]),t('new_snapshot','id:INTEGER PRIMARY KEY,val:TEXT',[(1,'a'),(2,'b'),(4,'d'),(5,None)])],
    '''SELECT o.id AS id,CASE WHEN n.id IS NULL THEN 'removed' ELSE 'changed' END AS change_kind,
           o.val AS old_value,n.val AS new_value
    FROM old_snapshot o LEFT JOIN new_snapshot n ON n.id=o.id
    WHERE n.id IS NULL OR o.val<>n.val
       OR (o.val IS NULL AND n.val IS NOT NULL)
       OR (o.val IS NOT NULL AND n.val IS NULL)
    UNION ALL
    SELECT n.id,'added',NULL,n.val
    FROM new_snapshot n LEFT JOIN old_snapshot o ON o.id=n.id
    WHERE o.id IS NULL
    ORDER BY id;''', [(2,'changed',None,'b'),(3,'removed','c',None),(4,'added',None,'d')],
    'Two disjoint LEFT JOIN branches emulate a full comparison. Presence is tested using the primary key; value differences explicitly include NULL transitions.',
    'old.val <> new.val misses NULL changes. COALESCE to a magic string conflates real data with a sentinel.',
    'On PostgreSQL, how would FULL OUTER JOIN and IS DISTINCT FROM shorten the query?')
add('Reconcile duplicate counts rather than just distinct rows', 'Set and multiset reconciliation', 'Hard', 'select', 'Original practice exercise',
    'Return keys whose multiplicity differs between two bags, with delta = new_count - old_count. NULL is a valid key. Suppress zero deltas.',
    [t('old_bag','key_name:TEXT',[('a',),('a',),('b',),(None,)]),t('new_bag','key_name:TEXT',[('a',),('b',),('b',),('c',),(None,),(None,)])],
    '''WITH signed AS (
      SELECT key_name,-1 AS delta FROM old_bag
      UNION ALL SELECT key_name,1 FROM new_bag
    )
    SELECT key_name,SUM(delta) AS delta FROM signed
    GROUP BY key_name HAVING SUM(delta)<>0
    ORDER BY CASE WHEN key_name IS NULL THEN 0 ELSE 1 END,key_name;''', [(None,1),('a',-1),('b',1),('c',1)],
    'Treat every old occurrence as minus one and every new occurrence as plus one, then add per key. GROUP BY also collects NULL keys together.',
    'EXCEPT with distinct semantics can hide multiplicity changes for a and b. UNION would erase repeated signed occurrences.',
    'How would you return actual surplus physical rows if the bags also had stable row IDs?')
add('Find customers covering every required product', 'Relational division and set equality', 'Hard', 'allproducts', 'Adapted pattern with duplicates, extras, and a master table',
    'Return registered customers who bought every required product. Extra purchases are allowed; repeated purchases do not help. When the required set is empty, every registered customer qualifies.',
    [t('customers','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,),(4,)]),t('required','product:TEXT PRIMARY KEY',[('A',),('B',)]),t('purchases','customer_id:INTEGER,product:TEXT',[(1,'A'),(1,'A'),(1,'B'),(1,'X'),(2,'A'),(2,'A'),(3,'A'),(3,'B')])],
    '''SELECT c.id FROM customers c
    WHERE NOT EXISTS (
      SELECT 1 FROM required r WHERE NOT EXISTS (
        SELECT 1 FROM purchases p WHERE p.customer_id=c.id AND p.product=r.product
      )
    ) ORDER BY c.id;''', [(1,),(3,)],
    'Double NOT EXISTS says there is no required product missing from this customer. It naturally handles duplicate purchases and an empty requirement set.',
    'Counting all purchased products can confuse duplicates or extras with coverage. Starting from purchases loses customers with no purchases under empty requirements.',
    'Why is the empty-set result called vacuous truth? When might the business rule deliberately reject it?')
add('Find customers whose basket exactly equals the required set', 'Relational division and set equality', 'Hard', 'allproducts', 'Original extension from containment to equality',
    'Return customers whose distinct purchased products equal the required set: no missing product and no extra product. Products and customer IDs are non-null. Duplicate purchases are irrelevant.',
    [t('customers','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,),(4,)]),t('required','product:TEXT PRIMARY KEY',[('A',),('B',)]),t('purchases','customer_id:INTEGER,product:TEXT',[(1,'A'),(1,'B'),(1,'X'),(2,'A'),(3,'A'),(3,'A'),(3,'B')])],
    '''SELECT c.id FROM customers c
    WHERE NOT EXISTS (
      SELECT 1 FROM required r WHERE NOT EXISTS (
        SELECT 1 FROM purchases p WHERE p.customer_id=c.id AND p.product=r.product
      )
    ) AND NOT EXISTS (
      SELECT 1 FROM purchases p WHERE p.customer_id=c.id AND NOT EXISTS (
        SELECT 1 FROM required r WHERE r.product=p.product
      )
    ) ORDER BY c.id;''', [(3,)],
    'Set equality needs containment in both directions. Coverage alone permits customer 1, whose basket includes X.',
    'Matching the count of distinct products is insufficient: a basket {A,X} has the same cardinality as {A,B}.',
    'With empty requirements, only customers with empty baskets should qualify.')
add('Find pairs of customers with identical baskets including empty ones', 'Relational division and set equality', 'Hard', 'pgsubquery', 'Original practice exercise',
    'Return customer pairs a < b whose distinct baskets are identical. Include pairs of empty baskets. Product keys are non-null; repeated basket rows count once.',
    [t('customers','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,),(4,),(5,)]),t('basket','customer_id:INTEGER,product:TEXT',[(1,'A'),(1,'A'),(1,'B'),(2,'B'),(2,'A'),(3,'A')])],
    '''SELECT a.id AS a,b.id AS b FROM customers a JOIN customers b ON a.id<b.id
    WHERE NOT EXISTS (
      SELECT 1 FROM basket x WHERE x.customer_id=a.id AND NOT EXISTS (
        SELECT 1 FROM basket y WHERE y.customer_id=b.id AND y.product=x.product
      )
    ) AND NOT EXISTS (
      SELECT 1 FROM basket y WHERE y.customer_id=b.id AND NOT EXISTS (
        SELECT 1 FROM basket x WHERE x.customer_id=a.id AND x.product=y.product
      )
    ) ORDER BY a.id,b.id;''', [(1,2),(4,5)],
    'Compare missing members in both directions for every candidate pair. Empty baskets pass both tests without special serialization.',
    'Concatenating products can collide, depend on ordering, or silently drop empty baskets. Equal counts do not establish equal contents.',
    'How would you change this to compare multisets where duplicate quantities matter?')
add('Find students who never scored an exam extreme', 'Universal conditions and exclusion', 'Hard', 'pgsubquery', 'Original practice exercise',
    'A quiet student took at least one exam and never tied for the minimum or maximum score in any exam they took. Return quiet student IDs. Scores are non-null and unique by student and exam. Students with no exams are excluded.',
    [t('students','id:INTEGER PRIMARY KEY',[(1,),(2,),(3,),(4,),(5,)]),t('scores','exam_id:INTEGER,student_id:INTEGER,score:INTEGER',[(1,1,10),(1,2,20),(1,3,30),(1,4,30),(2,1,40),(2,2,50),(2,3,60),(2,4,50)])],
    '''WITH limits AS (
      SELECT exam_id,MIN(score) AS lo,MAX(score) AS hi FROM scores GROUP BY exam_id
    )
    SELECT s.id FROM students s
    WHERE EXISTS (SELECT 1 FROM scores x WHERE x.student_id=s.id)
      AND NOT EXISTS (
        SELECT 1 FROM scores x JOIN limits l ON l.exam_id=x.exam_id
        WHERE x.student_id=s.id AND (x.score=l.lo OR x.score=l.hi)
      ) ORDER BY s.id;''', [(2,)],
    'First derive each exam extreme, then exclude anyone appearing at either extreme in any exam. The participation check excludes student 5.',
    'Filtering individual non-extreme rows still leaves student 4 because they were non-extreme in exam 2 but maximal in exam 1.',
    'In an exam with one participant, that participant is both minimum and maximum.')
add('Combine duplicate and unique conditions at different grains', 'Independent grouping grains', 'Hard', 'insurance', 'Adapted pattern with fresh integer amounts',
    'Sum current_value for policies whose prior_value occurs more than once across all policies, but whose (lat,lon) pair occurs exactly once across all policies. Locations and values are non-null.',
    [t('policies','id:INTEGER PRIMARY KEY,prior_value:INTEGER,current_value:INTEGER,lat:INTEGER,lon:INTEGER',[(1,10,5,1,1),(2,20,20,2,2),(3,10,30,2,2),(4,10,40,4,4),(5,99,7,5,5)])],
    '''WITH flagged AS (
      SELECT *,COUNT(*) OVER (PARTITION BY prior_value) AS prior_count,
               COUNT(*) OVER (PARTITION BY lat,lon) AS location_count FROM policies
    )
    SELECT COALESCE(SUM(current_value),0) AS total FROM flagged
    WHERE prior_count>1 AND location_count=1;''', [(45,)],
    'Compute independent frequencies on the original population. Both flags must hold for a policy to contribute.',
    'Filtering by duplicated prior value before counting locations makes policy 3 appear unique because policy 2 has already been removed.',
    'Why can concatenating latitude and longitude be an unsafe grouping key?')
add('Explain peer expansion in ROWS versus RANGE', 'Window frames and peer rows', 'Medium', 'pgwindow', 'Original semantics exercise',
    'Return each transaction with two cumulative sums: row_total follows (at,id) one row at a time; peer_total includes every transaction with timestamp <= the current timestamp. The two transactions at time 1 must share peer_total.',
    [t('tx','id:INTEGER PRIMARY KEY,at:INTEGER,amount:INTEGER',[(1,1,10),(2,1,20),(3,2,5)])],
    '''SELECT id,
      SUM(amount) OVER (ORDER BY at,id ROWS UNBOUNDED PRECEDING) AS row_total,
      SUM(amount) OVER (ORDER BY at RANGE UNBOUNDED PRECEDING) AS peer_total
    FROM tx ORDER BY at,id;''', [(1,10,30),(2,30,30),(3,35,35)],
    'ROWS follows individual row positions under a total ordering. RANGE treats equal ordering values as peers.',
    'Adding id to the RANGE ordering changes peer groups. Leaving the frame implicit may produce timestamp-wide jumps when row-by-row accumulation was intended.',
    'What total ordering is needed if two transactions share a timestamp?')
add('Get the true last value rather than the last value so far', 'Window frames and peer rows', 'Medium', 'pgwindow', 'Original semantics exercise',
    'Return every event with the final value for its user. Final means greatest (at,id), and a final NULL must stay NULL. Do not collapse the event rows.',
    [t('events','id:INTEGER PRIMARY KEY,user_id:INTEGER,at:INTEGER,val:INTEGER',[(1,1,1,10),(2,1,2,5),(3,2,1,7),(4,2,2,None)])],
    '''SELECT id,LAST_VALUE(val) OVER (
      PARTITION BY user_id ORDER BY at,id
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS final_value FROM events ORDER BY id;''', [(1,5),(2,5),(3,None),(4,None)],
    'The frame must reach the partition end. The function respects a genuinely NULL final observation.',
    'The default ordered frame ends at the current peer group, so LAST_VALUE often returns the current value. MAX is not the last value.',
    'How would the question change if it asked for the last non-null value?')
add('Forward fill NULLs even when values decrease', 'Window frames and missing values', 'Hard', 'window', 'Original practice exercise',
    'For each user, carry the latest non-null value forward in timestamp and ID order. Leading NULLs remain NULL. Values may decrease or be negative.',
    [t('readings','id:INTEGER PRIMARY KEY,user_id:INTEGER,at:INTEGER,val:INTEGER',[(1,1,1,None),(2,1,2,10),(3,1,3,None),(4,1,4,3),(5,1,5,None),(6,2,1,-2),(7,2,2,None)])],
    '''WITH g AS (
      SELECT *,COUNT(val) OVER (PARTITION BY user_id ORDER BY at,id ROWS UNBOUNDED PRECEDING) AS grp FROM readings
    )
    SELECT id,MAX(val) OVER (PARTITION BY user_id,grp) AS filled_value FROM g ORDER BY id;''', [(1,None),(2,10),(3,10),(4,3),(5,3),(6,-2),(7,-2)],
    'Each non-null value starts a new count group. Within a group there is exactly one non-null value, which MAX can propagate.',
    'A running MAX over the whole user keeps 10 after the real value decreases to 3.',
    'If NULL means an explicit reset rather than missing data, is forward fill appropriate?')
add('Compute a calendar rolling average with missing days', 'Calendar completion and rolling windows', 'Hard', 'restaurant', 'Original extension with missing days and a shorter window',
    'For report days 1 through 5, return complete three-calendar-day windows ending at days 3,4,5. Missing days have zero revenue. Multiple sales per day must first aggregate. Return day, window_total, and average rounded to two decimals.',
    [t('sales','id:INTEGER PRIMARY KEY,day_no:INTEGER,amount:INTEGER',[(1,1,10),(2,1,20),(3,3,60),(4,5,30)])],
    '''WITH RECURSIVE calendar(day_no) AS (
      SELECT 1 UNION ALL SELECT day_no+1 FROM calendar WHERE day_no<5
    ), totals AS (SELECT day_no,SUM(amount) AS amount FROM sales GROUP BY day_no),
    daily AS (
      SELECT c.day_no,COALESCE(t.amount,0) AS amount FROM calendar c LEFT JOIN totals t ON t.day_no=c.day_no
    ), rolled AS (
      SELECT day_no,SUM(amount) OVER (ORDER BY day_no ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS window_total FROM daily
    )
    SELECT day_no,window_total,ROUND(window_total/3.0,2) AS average
    FROM rolled WHERE day_no>=3 ORDER BY day_no;''', [(3,90,30.0),(4,60,20.0),(5,90,30.0)],
    'Densify the calendar and aggregate transaction grain before a row window. Only then do three rows mean three calendar days.',
    'Three preceding transactions or three observed days do not represent three calendar days. Filtering early removes window history.',
    'How would a real calendar table account for business days or daylight-saving boundaries?')
add('Count distinct active users across a rolling calendar window', 'Calendar completion and rolling windows', 'Hard', 'select', 'Original practice exercise',
    'Return distinct active users for each report day 1 through 4, considering that day and the previous two calendar days. Duplicate user events count once. There are no events before day 1.',
    [t('calendar','day_no:INTEGER PRIMARY KEY',[(1,),(2,),(3,),(4,)]),t('activity','user_id:INTEGER,day_no:INTEGER',[(1,1),(1,2),(1,2),(2,2),(3,4)])],
    '''SELECT c.day_no,(
      SELECT COUNT(DISTINCT a.user_id) FROM activity a
      WHERE a.day_no BETWEEN c.day_no-2 AND c.day_no
    ) AS active_users FROM calendar c ORDER BY c.day_no;''', [(1,1),(2,2),(3,2),(4,3)],
    'Distinctness is evaluated over the whole window, not independently for each day. Correlation provides a clear portable reference solution.',
    'Summing daily distinct counts double-counts users active on multiple days. COUNT(DISTINCT ...) as a window aggregate is not available in every SQL engine.',
    'For large data, how could per-user active intervals and sweep lines avoid repeated scans?')
add('Maintain a cumulative distinct count without a distinct window aggregate', 'Window frames and missing values', 'Hard', 'window', 'Original practice exercise',
    'In (at,id) event order, return the cumulative number of distinct non-null user IDs seen. NULL users contribute nothing. Repeated users do not increase the total.',
    [t('events','id:INTEGER PRIMARY KEY,at:INTEGER,user_id:INTEGER',[(1,1,8),(2,1,8),(3,2,9),(4,3,None),(5,4,8),(6,5,10)])],
    '''WITH marked AS (
      SELECT *,ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY at,id) AS occurrence FROM events
    )
    SELECT id,SUM(CASE WHEN user_id IS NOT NULL AND occurrence=1 THEN 1 ELSE 0 END)
      OVER (ORDER BY at,id ROWS UNBOUNDED PRECEDING) AS distinct_users
    FROM marked ORDER BY at,id;''', [(1,1),(2,1),(3,2),(4,2),(5,2),(6,3)],
    'Mark only each user first occurrence, then accumulate those markers. The explicit NULL exclusion matches COUNT(DISTINCT user_id) semantics.',
    'A running count of events includes repeats. DENSE_RANK over user_id imposes user-value order, not first-arrival order.',
    'Why does first-occurrence marking fail for a sliding distinct window when old users leave the window?')
add('Compute group medians without losing duplicate observations', 'Order statistics and weighted distributions', 'Hard', 'window', 'Original practice exercise',
    'Return the numeric median salary per company, averaging the two central observations for even-size groups. Equal salaries are separate observations. Salaries are non-null.',
    [t('employees','id:INTEGER PRIMARY KEY,company:TEXT,salary:INTEGER',[(1,'A',10),(2,'A',10),(3,'A',30),(4,'A',90),(5,'B',5),(6,'B',15),(7,'B',100)])],
    '''WITH ordered AS (
      SELECT *,ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary,id) AS rn,
               COUNT(*) OVER (PARTITION BY company) AS n FROM employees
    )
    SELECT company,AVG(salary*1.0) AS median FROM ordered
    WHERE rn BETWEEN (n+1)/2 AND (n+2)/2
    GROUP BY company ORDER BY company;''', [('A',20.0),('B',15.0)],
    'Integer division identifies one or two central row positions. A deterministic ID tie-break preserves observation identities.',
    'DENSE_RANK numbers distinct salary values rather than employees, changing the median when salaries repeat.',
    'If you need the employee records at the median instead of a scalar median, what should be returned for even counts?')
add('Find the median from value frequencies without expanding rows', 'Order statistics and weighted distributions', 'Hard', 'window', 'Original practice exercise',
    'Return the median of the represented multiset. Each frequency is a positive integer; value keys are unique. Avoid generating one row per observation.',
    [t('frequencies','val:INTEGER PRIMARY KEY,freq:INTEGER',[(10,2),(20,1),(30,3)])],
    '''WITH bounds AS (
      SELECT val,freq,SUM(freq) OVER (ORDER BY val ROWS UNBOUNDED PRECEDING) AS hi,
                      SUM(freq) OVER () AS n FROM frequencies
    ), positions AS (
      SELECT (SUM(freq)+1)/2 AS p FROM frequencies
      UNION ALL SELECT (SUM(freq)+2)/2 FROM frequencies
    )
    SELECT AVG(b.val*1.0) AS median
    FROM positions p JOIN bounds b ON p.p>b.hi-b.freq AND p.p<=b.hi;''', [(25.0,)],
    'Each value owns a cumulative rank interval. Locate both central positions within those intervals; UNION ALL retains two equal middle positions for odd counts.',
    'Taking the median of distinct values ignores frequency. Expanding very large frequencies wastes work.',
    'How would the rank target change for a percentile other than the median?')
add('Find the last person in a capacity-limited boarding prefix', 'Prefix constraints and cumulative state', 'Medium', 'bus', 'Adapted problem with fresh data and explicit stop semantics',
    'People board in ascending turn. Boarding stops at the first person who would exceed capacity 1000; later lighter people cannot skip ahead. Weights are positive and turns are unique. Return the final admitted person, or no row if nobody fits.',
    [t('queue','turn:INTEGER PRIMARY KEY,name:TEXT,weight:INTEGER',[(1,'Ana',400),(2,'Ben',350),(3,'Cy',250),(4,'Di',1),(5,'Eli',10)])],
    '''WITH totals AS (
      SELECT *,SUM(weight) OVER (ORDER BY turn ROWS UNBOUNDED PRECEDING) AS cumulative FROM queue
    )
    SELECT turn,name FROM totals WHERE cumulative<=1000 ORDER BY turn DESC LIMIT 1;''', [(3,'Cy')],
    'Positive weights make cumulative load monotonic, so eligible rows form a prefix. Descending turn chooses its final member.',
    'Filtering each person by individual weight does not enforce the shared capacity. The query relies on positivity and stop-at-first-failure semantics.',
    'If skipping people is allowed, why is this no longer a simple prefix problem?')
add('Reset running totals at reset events', 'Prefix constraints and cumulative state', 'Hard', 'window', 'Original practice exercise',
    'Return each event with its accumulated amount since the most recent reset. Reset rows have amount zero and reset the displayed total to zero. Amounts may be negative. Events have a unique sequence number.',
    [t('events','seq:INTEGER PRIMARY KEY,is_reset:INTEGER,amount:INTEGER',[(1,0,5),(2,0,3),(3,1,0),(4,0,4),(5,0,-1),(6,1,0),(7,0,2)])],
    '''WITH grouped AS (
      SELECT *,SUM(is_reset) OVER (ORDER BY seq ROWS UNBOUNDED PRECEDING) AS grp FROM events
    )
    SELECT seq,SUM(amount) OVER (PARTITION BY grp ORDER BY seq ROWS UNBOUNDED PRECEDING) AS running_total
    FROM grouped ORDER BY seq;''', [(1,5),(2,8),(3,0),(4,4),(5,3),(6,0),(7,2)],
    'A running count of reset events creates partitions. Each partition receives its own cumulative amount.',
    'Subtracting a global running minimum is unrelated to resets. Filtering reset rows before assigning groups removes the boundaries.',
    'If a reset row also contains an amount, should that amount be included before or after the reset?')
add('Detect repeated values by row adjacency rather than ID arithmetic', 'Gaps and islands', 'Medium', 'consecutive', 'Original extension distinguishing row adjacency from consecutive IDs',
    'Return non-null values appearing in at least three consecutive observations ordered by seq. seq is unique but may have gaps. Consecutive means adjacent rows, not seq + 1. Return each qualifying value once.',
    [t('logs','seq:INTEGER PRIMARY KEY,val:INTEGER',[(10,7),(20,7),(40,7),(50,8),(60,7),(70,8),(80,8),(90,8)])],
    '''WITH g AS (
      SELECT val,ROW_NUMBER() OVER (ORDER BY seq)
        -ROW_NUMBER() OVER (PARTITION BY val ORDER BY seq) AS island FROM logs
    )
    SELECT DISTINCT val FROM g WHERE val IS NOT NULL
    GROUP BY val,island HAVING COUNT(*)>=3 ORDER BY val;''', [(7,),(8,)],
    'The difference between global and per-value row positions is constant within each uninterrupted value run. Group by both the value and the difference.',
    'Joining seq to seq+1 fails on sparse identifiers. Grouping by the difference alone can merge runs from different values.',
    'If NULL itself is a meaningful repeated value, how should the query change?')
add('Swap neighboring seats when seat IDs are sparse', 'Positional pairing', 'Hard', 'seats', 'Original extension using position rather than ID parity',
    'Order seats by seat_id and swap the occupants of each neighboring pair. Keep seat IDs fixed. An odd last occupant stays. Seat IDs need not start at 1 or be consecutive; occupants are non-null.',
    [t('seats','seat_id:INTEGER PRIMARY KEY,occupant:TEXT',[(10,'Ana'),(20,'Ben'),(40,'Cy'),(70,'Di'),(90,'Eli')])],
    '''WITH positioned AS (
      SELECT *,ROW_NUMBER() OVER (ORDER BY seat_id) AS pos FROM seats
    )
    SELECT a.seat_id,COALESCE(b.occupant,a.occupant) AS occupant
    FROM positioned a LEFT JOIN positioned b
      ON b.pos=CASE WHEN a.pos%2=1 THEN a.pos+1 ELSE a.pos-1 END
    ORDER BY a.seat_id;''', [(10,'Ben'),(20,'Ana'),(40,'Di'),(70,'Cy'),(90,'Eli')],
    'Pair ordinal positions, not numeric IDs. The unmatched last position falls back to its current occupant.',
    'seat_id +/- 1 and ID parity assume dense identifiers. A nullable occupant would require checking partner presence instead of COALESCE.',
    'How would the logic differ for rotating groups of three instead of swapping pairs?')
add('Choose tournament winners when players occupy either match column', 'Role unpivoting and tie rules', 'Hard', 'select', 'Original practice exercise',
    'Return the winning player for every group by total match score. A player can appear as either first_player or second_player. Include registered players with no matches as zero. Break total-score ties by smaller player ID. Each match belongs within one group.',
    [t('players','id:INTEGER PRIMARY KEY,group_id:INTEGER',[(1,1),(2,1),(3,1),(4,2),(5,2)]),t('matches','id:INTEGER PRIMARY KEY,first_player:INTEGER,second_player:INTEGER,first_score:INTEGER,second_score:INTEGER',[(1,1,2,3,1),(2,2,3,2,3)])],
    '''WITH points AS (
      SELECT first_player AS player_id,first_score AS score FROM matches
      UNION ALL SELECT second_player,second_score FROM matches
    ), totals AS (
      SELECT p.id,p.group_id,COALESCE(SUM(x.score),0) AS score
      FROM players p LEFT JOIN points x ON x.player_id=p.id GROUP BY p.id,p.group_id
    ), ranked AS (
      SELECT *,ROW_NUMBER() OVER (PARTITION BY group_id ORDER BY score DESC,id) AS rn FROM totals
    )
    SELECT group_id,id AS winner_id,score FROM ranked WHERE rn=1 ORDER BY group_id;''', [(1,1,3),(2,4,0)],
    'Unpivot both participant roles before aggregation. Only after scores are complete does the stated tie rule select a winner.',
    'Joining only first_player misses half the contributions. UNION can erase two legitimate equal-scoring match contributions.',
    'How would your result differ if the task asked for every tied winner?')
add('Compute cohort retention with a fixed signup denominator', 'Grain and denominator traps', 'Hard', 'select', 'Original practice exercise',
    'Return day-one retention for each signup-day cohort: the fraction of its registered users with at least one activity exactly one day after signup. Duplicate activity rows count once; inactive users stay in the denominator. Round to two decimals.',
    [t('users','id:INTEGER PRIMARY KEY,signup_day:INTEGER',[(1,1),(2,1),(3,1),(4,2),(5,2)]),t('activity','user_id:INTEGER,day_no:INTEGER',[(1,2),(1,2),(2,3),(4,3),(5,3)])],
    '''SELECT u.signup_day,ROUND(AVG(CASE WHEN EXISTS (
      SELECT 1 FROM activity a WHERE a.user_id=u.id AND a.day_no=u.signup_day+1
    ) THEN 1.0 ELSE 0.0 END),2) AS retention
    FROM users u GROUP BY u.signup_day ORDER BY u.signup_day;''', [(1,0.33),(2,1.0)],
    'Each signup contributes one indicator to the average. The source population is the cohort, not the people who happened to return.',
    'An inner join removes inactive users and repeated activity overweights active users. Consecutive activity days are not necessarily day-one retention.',
    'For unfinished cohorts, how should the report exclude users whose day-one observation window has not closed?')
add('Find consecutive over-limit months across a year boundary', 'Calendar adjacency and preaggregation', 'Hard', 'window', 'Original practice exercise',
    'Return accounts whose credited total exceeds their limit in two consecutive calendar months. month_index is year*12 + month-1, so December and January are adjacent. Aggregate credits by account and month first. Missing months are not over-limit; equals the limit is not over-limit.',
    [t('accounts','id:INTEGER PRIMARY KEY,monthly_limit:INTEGER',[(1,100),(2,100),(3,100)]),t('credits','account_id:INTEGER,month_index:INTEGER,amount:INTEGER',[(1,24299,60),(1,24299,60),(1,24300,110),(2,24299,120),(2,24301,130),(3,24299,100),(3,24300,150)])],
    '''WITH monthly AS (
      SELECT c.account_id,c.month_index,SUM(c.amount) AS total
      FROM credits c GROUP BY c.account_id,c.month_index
    ), over_limit AS (
      SELECT m.* FROM monthly m JOIN accounts a ON a.id=m.account_id WHERE m.total>a.monthly_limit
    ), adjacent AS (
      SELECT *,LAG(month_index) OVER (PARTITION BY account_id ORDER BY month_index) AS prev FROM over_limit
    )
    SELECT DISTINCT account_id FROM adjacent WHERE month_index=prev+1 ORDER BY account_id;''', [(1,)],
    'Monthly aggregation precedes threshold testing. Month ordinals make year transitions and missing months explicit.',
    'Two over-limit observations can be separated by months. Comparing raw month numbers falsely treats December to January as a nonconsecutive transition.',
    'How would you derive month_index from actual dates in PostgreSQL or SQL Server?')
add('Find all descendants without looping on cyclic relationships', 'Recursive reachability', 'Hard', 'pgrecursive', 'Original practice exercise',
    'Return all IDs reachable below manager 1 through the reports edges, excluding manager 1 itself. Data can be cyclic and duplicated; an employee may have more than one incoming edge.',
    [t('reports','manager_id:INTEGER,employee_id:INTEGER',[(1,2),(2,3),(3,1),(2,4),(1,2),(5,6)])],
    '''WITH RECURSIVE reachable(id) AS (
      SELECT 1
      UNION
      SELECT r.employee_id FROM reports r JOIN reachable x ON r.manager_id=x.id
    )
    SELECT id FROM reachable WHERE id<>1 ORDER BY id;''', [(2,),(3,),(4,)],
    'Deduplicate only the reachable identity. Every reachable ID can enter the state once, even through cycles and multiple paths.',
    'A fixed number of self joins assumes a maximum depth. UNION ALL with no visited-state guard keeps expanding the 1 to 2 to 3 to 1 cycle.',
    'If you must show each full reporting path, how will you prevent revisiting a node already in that path?')
add('Classify tree nodes with root precedence', 'Hierarchy classification', 'Medium', 'tree', 'Adapted pattern with multiple rooted trees including a singleton',
    'Classify each node Root, Inner, or Leaf. A root has no parent and must be Root even if it has no children. The input is a valid forest with non-null IDs and nullable parent_id.',
    [t('nodes','id:INTEGER PRIMARY KEY,parent_id:INTEGER',[(1,None),(2,1),(3,1),(4,2),(9,None)])],
    '''SELECT n.id,CASE
      WHEN n.parent_id IS NULL THEN 'Root'
      WHEN EXISTS (SELECT 1 FROM nodes c WHERE c.parent_id=n.id) THEN 'Inner'
      ELSE 'Leaf' END AS node_type
    FROM nodes n ORDER BY n.id;''', [(1,'Root'),(2,'Inner'),(3,'Leaf'),(4,'Leaf'),(9,'Root')],
    'Test root status before child existence so the singleton root is classified correctly. EXISTS avoids expanding parents with multiple children.',
    'id NOT IN (SELECT parent_id ...) is poisoned by root NULLs. Checking leaf before root misclassifies a singleton.',
    'How would you report orphan nodes whose non-null parent ID is missing from the master?')
add('Find ordered funnel completions rather than mere event presence', 'Ordered event matching', 'Hard', 'pgsubquery', 'Original practice exercise',
    'Return users who have a view, then a later add, then a later buy. Timestamps must strictly increase. Repeated attempts are allowed and any valid sequence qualifies. Merely having all three event kinds is insufficient.',
    [t('events','id:INTEGER PRIMARY KEY,user_id:INTEGER,kind:TEXT,at:INTEGER',[(1,1,'view',1),(2,1,'buy',2),(3,1,'add',3),(4,1,'buy',4),(5,2,'buy',1),(6,2,'add',2),(7,2,'view',3),(8,3,'view',1),(9,3,'add',1),(10,3,'buy',2)])],
    '''SELECT DISTINCT v.user_id FROM events v
    WHERE v.kind='view' AND EXISTS (
      SELECT 1 FROM events a WHERE a.user_id=v.user_id AND a.kind='add' AND a.at>v.at
        AND EXISTS (
          SELECT 1 FROM events b WHERE b.user_id=a.user_id AND b.kind='buy' AND b.at>a.at
        )
    ) ORDER BY v.user_id;''', [(1,)],
    'Correlated existence checks preserve the ordering relation for a complete sequence. User 1 can use the later buy even though an earlier buy was out of order.',
    'COUNT(DISTINCT kind)=3 admits users 2 and 3. Taking only each kind first event can miss a valid later retry.',
    'How would you impose a maximum total funnel duration or require all steps within one session?')
add('Allocate supply to demand in FIFO order without a cursor', 'Cumulative interval matching and FIFO', 'Hard', 'supply', 'Adapted allocation pattern with fresh data',
    'Supplies are available before all demands. Consume supplies and fulfill demands in ascending ID order. Quantities are positive and total supply is sufficient. Return demand_id, supply_id, and allocated quantity for every nonzero allocation.',
    [t('supplies','id:INTEGER PRIMARY KEY,qty:INTEGER',[(1,5),(2,4),(3,6)]),t('demands','id:INTEGER PRIMARY KEY,qty:INTEGER',[(1,7),(2,5)])],
    '''WITH s AS (
      SELECT id,qty,SUM(qty) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi FROM supplies
    ), d AS (
      SELECT id,qty,SUM(qty) OVER (ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi FROM demands
    )
    SELECT d.id AS demand_id,s.id AS supply_id,
      CASE WHEN s.hi<d.hi THEN s.hi ELSE d.hi END
        -CASE WHEN s.hi-s.qty>d.hi-d.qty THEN s.hi-s.qty ELSE d.hi-d.qty END AS allocated
    FROM s JOIN d ON s.hi>d.hi-d.qty AND d.hi>s.hi-s.qty
    ORDER BY d.id,s.id;''', [(1,1,5),(1,2,2),(2,2,2),(2,3,3)],
    'Give supplies and demands half-open spans on a cumulative quantity axis. Their overlap length is the allocation, including partial splits.',
    'An equality join on cumulative endpoints misses split allocations. This formulation does not enforce receipt-before-demand time unless availability is separately guaranteed.',
    'How would you handle shortage, multiple products, or receipts arriving after a demand?')
add('Value remaining FIFO inventory with a partially consumed batch', 'Cumulative interval matching and FIFO', 'Hard', 'fifo', 'Simplified adaptation with no returns or backorders',
    'For each product, return remaining quantity and FIFO inventory value after all movements. IN rows have positive quantity and a unit cost; OUT rows have positive quantity and NULL cost. IDs define chronology. Inventory never goes negative. There are no returns. Equal costs do not identify equal batches.',
    [t('movements','id:INTEGER PRIMARY KEY,product:TEXT,kind:TEXT,qty:INTEGER,cost:INTEGER',[(1,'A','IN',5,10),(2,'A','IN',4,20),(3,'A','OUT',7,None),(4,'A','IN',6,30),(5,'A','OUT',5,None),(6,'B','IN',2,7),(7,'B','OUT',2,None)])],
    '''WITH incoming AS (
      SELECT *,SUM(qty) OVER (PARTITION BY product ORDER BY id ROWS UNBOUNDED PRECEDING) AS hi
      FROM movements WHERE kind='IN'
    ), sold AS (
      SELECT product,SUM(CASE WHEN kind='OUT' THEN qty ELSE 0 END) AS qty
      FROM movements GROUP BY product
    ), leftovers AS (
      SELECT i.product,i.cost,CASE
        WHEN i.hi<=s.qty THEN 0
        WHEN i.hi-i.qty>=s.qty THEN i.qty
        ELSE i.hi-s.qty END AS remaining
      FROM incoming i JOIN sold s ON s.product=i.product
    )
    SELECT product,SUM(remaining) AS remaining_qty,SUM(remaining*cost) AS inventory_value
    FROM leftovers GROUP BY product ORDER BY product;''', [('A',3,90),('B',0,0)],
    'Total sold consumes a prefix of each product cumulative receipt axis. Only the unconsumed suffix of each priced batch contributes value.',
    'Multiplying net quantity by an average or latest cost loses batch provenance. Fully consumed products must still return zero.',
    'How should returned stock acquire its cost? What validation is needed before accepting negative stock histories?')

# Alternative approaches with the same output contract.
QUESTIONS[5]['alternatives'].append(('Boundary flags instead of row-number subtraction', '''WITH d AS (SELECT DISTINCT value FROM observations),
p AS (SELECT value,LAG(value) OVER (ORDER BY value) AS prev FROM d),
g AS (SELECT value,SUM(CASE WHEN prev IS NULL OR value<>prev+1 THEN 1 ELSE 0 END)
      OVER (ORDER BY value ROWS UNBOUNDED PRECEDING) AS island FROM p)
SELECT MIN(value) AS start_value,MAX(value) AS end_value,COUNT(*) AS length
FROM g GROUP BY island ORDER BY start_value;'''))
QUESTIONS[16]['alternatives'].append(('Correlated latest eligible change', '''SELECT p.id,COALESCE((
  SELECT c.price FROM changes c WHERE c.product_id=p.id AND c.day_no<=5
  ORDER BY c.day_no DESC LIMIT 1
),10) AS price FROM products p ORDER BY p.id;'''))
QUESTIONS[22]['alternatives'].append(('Deduplicate eligible identities before aggregating', '''WITH eligible AS (
  SELECT DISTINCT invoice_id FROM tags WHERE tag='approved'
)
SELECT COALESCE(SUM(i.amount),0) AS approved_total
FROM invoices i JOIN eligible e ON e.invoice_id=i.id;'''))
QUESTIONS[25]['alternatives'].append(('Count coverage after intersecting with requirements', '''SELECT c.id FROM customers c
LEFT JOIN purchases p ON p.customer_id=c.id
LEFT JOIN required r ON r.product=p.product
GROUP BY c.id
HAVING COUNT(DISTINCT r.product)=(SELECT COUNT(*) FROM required)
ORDER BY c.id;'''))
QUESTIONS[38]['alternatives'].append(('Correlated prefix sum', '''SELECT q.turn,q.name FROM queue q
WHERE (SELECT SUM(p.weight) FROM queue p WHERE p.turn<=q.turn)<=1000
ORDER BY q.turn DESC LIMIT 1;'''))
QUESTIONS[40]['alternatives'].append(('Three adjacent row positions using LEAD', '''WITH n AS (
  SELECT val,LEAD(val,1) OVER (ORDER BY seq) AS v1,
             LEAD(val,2) OVER (ORDER BY seq) AS v2 FROM logs
)
SELECT DISTINCT val FROM n WHERE val=v1 AND val=v2 ORDER BY val;'''))

def clean_sql(sql):
    lines=textwrap.dedent(sql).strip().splitlines()
    tail=[len(line)-len(line.lstrip()) for line in lines[1:] if line.strip()]
    margin=min(tail,default=0)
    return '\n'.join([lines[0]]+[line[margin:] if line.strip() else '' for line in lines[1:]])

def literal(v):
    if v is None: return 'NULL'
    if isinstance(v, str): return "'" + v.replace("'", "''") + "'"
    return str(v)
def fixture_sql(q):
    parts=[]
    for tab in q['tables']:
        cols=',\n    '.join(name+' '+kind for name,kind in tab['columns'])
        parts.append(f"CREATE TABLE {tab['name']} (\n    {cols}\n);")
        if tab['rows']:
            vals=',\n    '.join('('+', '.join(literal(v) for v in row)+')' for row in tab['rows'])
            names=', '.join(name for name,_ in tab['columns'])
            parts.append(f"INSERT INTO {tab['name']} ({names}) VALUES\n    {vals};")
    return '\n\n'.join(parts)
def display(v):
    if v is None: return 'NULL'
    return str(v).replace('|','\\|')
def md_table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+
                     ['| '+' | '.join(display(v) for v in row)+' |' for row in rows])
def anchor(q):
    return q['id'].lower()+'-'+q['title'].lower().replace(' ','-')
def source_link(q):
    label,url=SOURCES[q['source']]
    prefix='Pattern reference' if q['origin'].startswith('Original') else 'Source pattern'
    return f"{q['origin']}. {prefix}: [{label}]({url})."
def outputs(q):
    with sqlite3.connect(':memory:') as db:
        db.executescript(fixture_sql(q))
        c=db.execute(q['sql'])
        return [d[0] for d in c.description],c.fetchall()
def main():
    from build_pyspark_docs import question_section, solution_section, write_guide
    for q in QUESTIONS:
        q['title']=q['title'].replace('-', ' ')
        q['sql']=clean_sql(q['sql'])
        q['alternatives']=[(name,clean_sql(sql)) for name,sql in q['alternatives']]
    assert len(QUESTIONS)==50
    headers={}
    for q in QUESTIONS:
        cols,actual=outputs(q)
        assert actual==q['expected'],f"{q['id']} expected {q['expected']} got {actual}"
        headers[q['id']]=cols
    sql_dir=ROOT/'sql';sql_dir.mkdir(exist_ok=True)
    question_parts=['# SQL Trick Questions and Sample Datasets',
      'Practice 50 SQL puzzles where the main challenge is identifying a hidden assumption, preserving the correct data grain, or recognizing a reusable pattern. Basic counts and ordinary highest-salary ranking questions are excluded.',
      '## How to practice',
      'Use one exercise per fresh database. Each question has its own runnable CREATE TABLE and INSERT statements, sample tables, and expected output. Solutions are in [SOLUTIONS.md](SOLUTIONS.md). Numbering matches across both documents. Expected rows are ordered as shown. Difficulty labels are editorial estimates for these variants, not source-platform ratings.',
      'The reference execution dialect is **SQLite 3.28 or newer**, available through Python standard library sqlite3. Every exercise also links to a PySpark DataFrame implementation with explicit input schemas. Most queries use broadly shared SQL constructs; dialect changes are listed in [SOLUTIONS.md](SOLUTIONS.md#dialect-and-data-conventions). Calendar days, elapsed minutes, and month ordinals are deliberately integers so the pattern is visible without engine-specific date syntax. Day ordinals are not YYYYMMDD values.',
      '## Pattern index',
      md_table(['ID','Question','Pattern','Difficulty'],[[q['id'],f"[{q['title']}](#{anchor(q)})",q['pattern'],q['difficulty']] for q in QUESTIONS])]
    solution_parts=['# SQL Trick Question Solutions',
      'Each solution answers the corresponding exercise in [QUESTIONS.md](QUESTIONS.md). Each exercise also includes a **PySpark DataFrame solution** and sample setup; start with [the PySpark guide](PYSPARK_GUIDE.md) for runtime setup and shared helpers. Read the question contract first: duplicate identity, time boundaries, allowed ties, missing rows, and NULL meaning determine whether the SQL is correct.',
      '## Dialect and data conventions',
      '- Tested reference dialect: SQLite 3.28 or newer. See VERIFICATION.md for the recorded runtime version. No database server or third-party package is required.\n- Integer `/` in the median queries must truncate for integer operands; `3.0` and `1.0` force fractional arithmetic where required. Adapt with FLOOR or integer division in another dialect.\n- SQL Server: remove the RECURSIVE keyword, use TOP or OFFSET/FETCH instead of LIMIT, use an appropriate string type instead of TEXT, and apply the engine recursion limits deliberately. Recursive UNION-based cycle handling needs a different implementation because SQL Server recursive CTE syntax and restrictions differ.\n- PostgreSQL: these CASE-based endpoint comparisons avoid reliance on SQLite scalar MIN/MAX. PostgreSQL offers LEAST/GREATEST and IS DISTINCT FROM as conveniences. This catalog does not claim engine-by-engine execution testing.\n- MySQL: use 8.0 or newer for window functions and recursive CTEs; median integer divisions need DIV or FLOOR.\n- Spark SQL: date and interval arithmetic differs, and recursive support depends on runtime. Treat the recursive exercises as requiring a supported engine or an explicit iterative implementation.\n- Text comparisons follow the database collation. Endpoints in the pair exercises are non-null and must use a consistent collation.\n- day_no denotes consecutive calendar-day ordinals; minute_no denotes elapsed-minute ordinals. month_index = year*12 + month-1. Convert actual DATE/TIMESTAMP data with dialect-appropriate functions and a declared timezone.\n- [start,end) intervals include start and exclude end. Positive-length intervals are assumed.\n- Fixture DDL is intentionally small; production constraints, indexes, and query plans must match real workload contracts.',
      '## Solution index',md_table(['ID','Solution','Pattern'],[[q['id'],f"[{q['title']}](#{anchor(q)})",q['pattern']] for q in QUESTIONS])]
    for q in QUESTIONS:
        ident=q['id']; fixture=fixture_sql(q)
        (sql_dir/f'{ident}_setup.sql').write_text(fixture+'\n',encoding='utf-8')
        (sql_dir/f'{ident}_solution.sql').write_text(q['sql']+'\n',encoding='utf-8')
        qp=[f"## {ident} {q['title']}",f"**Pattern:** {q['pattern']}\n\n**Difficulty:** {q['difficulty']}",source_link(q),q['prompt'],'### Sample data']
        for tab in q['tables']:
            qp.extend([f"**{tab['name']}**",md_table([name for name,_ in tab['columns']],tab['rows'])])
        qp.extend(['### SQL setup',f'```sql\n{fixture}\n```','### Expected output',md_table(headers[ident],q['expected']),question_section(q)])
        question_parts.extend(qp)
        sp=[f"## {ident} {q['title']}",f"**Pattern:** {q['pattern']}",f"[Question and dataset](QUESTIONS.md#{anchor(q)})",f"```sql\n{q['sql']}\n```",'### Why it works',q['explanation'],'### The trap',q['trap']]
        for i,(name,query) in enumerate(q['alternatives'],1):
            query=textwrap.dedent(query).strip()
            sp.extend([f'### Alternative {name}',f'```sql\n{query}\n```'])
            (sql_dir/f'{ident}_alternative_{i}.sql').write_text(query+'\n',encoding='utf-8')
        sp.extend(solution_section(q))
        sp.extend(['### Expected output',md_table(headers[ident],q['expected']),'### Interview follow up',q['followup'],source_link(q)])
        solution_parts.extend(sp)
    write_guide(QUESTIONS)
    (ROOT/'QUESTIONS.md').write_text('\n\n'.join(question_parts)+'\n',encoding='utf-8')
    (ROOT/'SOLUTIONS.md').write_text('\n\n'.join(solution_parts)+'\n',encoding='utf-8')
    (ROOT/'catalog.json').write_text(json.dumps(QUESTIONS,indent=2)+'\n',encoding='utf-8')
    used=sorted(set(q['source'] for q in QUESTIONS)|{'supplysolution','pgwindow','pgjoin','pgrecursive','expr','select'})
    sources='\n'.join(f"- [{SOURCES[s][0]}]({SOURCES[s][1]})" for s in used)
    readme=f'''# SQL Trick Question Catalog

50 exercises organized into {len(set(q['pattern'] for q in QUESTIONS))} patterns, with fresh datasets, expected outputs, and runnable SQL and PySpark DataFrame solutions.

- [Questions and sample datasets](QUESTIONS.md)
- [SQL and PySpark solutions and explanations](SOLUTIONS.md)
- [PySpark setup, helpers, and question index](PYSPARK_GUIDE.md)
- [PySpark verification results](PYSPARK_VERIFICATION.md)
- [Verification results](VERIFICATION.md)

The focus is reverse-pair deduplication, gaps and islands, nested intervals, temporal joins, anti joins, join multiplicity, relational division, window frames, rolling distinctness, medians, recursion, ordered funnels, and FIFO. Simple count questions and ordinary top-earner ranking exercises are excluded. Some solutions use COUNT or ROW_NUMBER as building blocks; their challenge is the surrounding semantics.

## Practice and verification

Use Python 3 with SQLite 3.28 or newer:

```sh
python3 verify.py
python3 verify.py --question Q13
```

To run a query manually, load its setup and solution into a fresh SQLite database:

```sh
sqlite3 :memory: '.read sql/Q13_setup.sql' '.read sql/Q13_solution.sql'
```

For PySpark, install `requirements-pyspark.txt` in a virtual environment with Java 17 available, then run `python pyspark_runner.py --question Q01`. See [the setup guide](PYSPARK_GUIDE.md) for full instructions. Every solution includes DataFrame code and explicit sample-data setup; the reverse-route exercise also includes a left-join alternative.

There are two main study documents. The sql folder contains extracted executable copies, catalog.json holds structured metadata and independent expected rows, build_catalog.py generates the documents, and verify.py checks queries and randomized edge cases. The SQL checks need no database server or third-party package. The PySpark checks use the separately installed runtime described above. Do not load all setup files into one database; exercises intentionally reuse table names.

Read the [dialect notes](SOLUTIONS.md#dialect-and-data-conventions) before translating queries to SQL Server, PostgreSQL, MySQL, or Spark SQL. Calendar and elapsed-time ordinals make the algorithm explicit. Actual DATE/TIMESTAMP conversions need the correct dialect and timezone.

## Research and scope

Researched on October 10, 2026. This is a curated catalog rather than a claim to enumerate every SQL puzzle on the internet. Questions were selected for a distinct conceptual trap, not merely a long query. Similar variants are included only when the additional condition changes the solution, such as set containment versus equality, row adjacency versus consecutive IDs, or interval packing versus complement and duration.

Public challenge pages, original author tutorials, and official database documentation provide the pattern references. Each exercise identifies whether it adapts a published problem or is an original extension/semantics exercise. All fixtures and solution prose are newly authored; source datasets and editorials are not copied. No employer attribution or claim of interview frequency is inferred. Some other LeetCode pages encountered during research required a subscription and were not used as verified problem statements.

Official documentation linked for an original exercise establishes the SQL construct or semantics; it does not claim that the exact exercise appeared in an interview. Verification covers the declared sample and targeted generated cases, not every possible input or production performance. Closest-match and correlated-window reference solutions prioritize clarity over scale.

## Source references

{sources}

## Pattern map

'''
    pattern_rows=[]
    for pat in dict.fromkeys(q['pattern'] for q in QUESTIONS):
        qs=[q for q in QUESTIONS if q['pattern']==pat]
        pattern_rows.append([pat,', '.join(f"[{q['id']}](QUESTIONS.md#{anchor(q)})" for q in qs)])
    readme+=md_table(['Pattern','Exercises'],pattern_rows)+'\n'
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
    (ROOT/'.gitignore').write_text('__pycache__/\n*.pyc\n*.db\n.DS_Store\n.venv/\nspark-warehouse/\nartifacts/\n',encoding='utf-8')
    if not (ROOT/'VERIFICATION.md').exists():
        (ROOT/'VERIFICATION.md').write_text('# SQL Catalog Verification\n\nVerification has not yet run. Execute python3 verify.py.\n',encoding='utf-8')
    print(f'Generated {len(QUESTIONS)} questions and {sum(len(q["alternatives"]) for q in QUESTIONS)} alternatives.')
if __name__=='__main__':main()
