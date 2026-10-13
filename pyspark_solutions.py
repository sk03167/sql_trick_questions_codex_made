"""DataFrame implementations of Q01–Q50; see PYSPARK_SOLUTIONS.md."""
from pyspark.sql import Window, functions as F


def prefix(window):
    return window.rowsBetween(Window.unboundedPreceding, Window.currentRow)


def pack_intervals(df, start='start_at', end='end_at'):
    """Pack touching/overlapping positive-length intervals, including nesting."""
    w = Window.orderBy(start, end, 'id')
    marked = df.withColumn('_previous_max', F.max(end).over(
        w.rowsBetween(Window.unboundedPreceding, -1)))
    marked = marked.withColumn('_fresh', F.when(
        F.col('_previous_max').isNull() | (F.col(start) > F.col('_previous_max')), 1).otherwise(0))
    grouped = marked.withColumn('_island', F.sum('_fresh').over(prefix(w)))
    return grouped.groupBy('_island').agg(
        F.min(start).alias(start), F.max(end).alias(end)).drop('_island')


def reachability(seeds, edges):
    """Distinct (root,node) closure; requires a configured checkpoint directory.

    seeds: root,node. edges: src,dst. No graph rows are collected to Python.
    Durable checkpoints bound plan growth; the caller owns their cleanup.
    """
    seen = seeds.distinct().checkpoint(eager=True)
    frontier = seen
    edges = edges.distinct()
    while True:
        candidates = (frontier.alias('f').join(edges.alias('e'),
            F.col('f.node') == F.col('e.src'))
            .select('f.root', F.col('e.dst').alias('node')).distinct())
        fresh = candidates.join(seen, ['root', 'node'], 'left_anti').checkpoint(eager=True)
        if fresh.isEmpty():
            return seen
        seen = seen.unionByName(fresh).checkpoint(eager=True)
        frontier = fresh


def q01(t):
    routes = t['routes']
    canonical = (routes.withColumn('_lo', F.least('src', 'dst'))
                 .withColumn('_hi', F.greatest('src', 'dst')))
    w = Window.partitionBy('_lo', '_hi', 'dist').orderBy('row_id')
    return (canonical.withColumn('_rn', F.row_number().over(w)).filter('_rn = 1')
            .select('row_id', 'src', 'dst', 'dist').orderBy('row_id'))


def q01_left_join(t):
    # A survivor has no smaller row_id with the same unordered endpoints/distance.
    a, b = t['routes'].alias('a'), t['routes'].alias('b')
    same_pair = (((F.col('a.src') == F.col('b.src')) & (F.col('a.dst') == F.col('b.dst'))) |
                 ((F.col('a.src') == F.col('b.dst')) & (F.col('a.dst') == F.col('b.src'))))
    condition = same_pair & (F.col('a.dist') == F.col('b.dist')) & (F.col('b.row_id') < F.col('a.row_id'))
    return (a.join(b, condition, 'left').filter(F.col('b.row_id').isNull())
            .select('a.*').orderBy('row_id'))


def q02(t):
    a, b = t['pairs'].alias('a'), t['pairs'].alias('b')
    condition = ((F.col('a.x') == F.col('b.y')) & (F.col('a.y') == F.col('b.x')) &
                 (F.col('a.id') != F.col('b.id')))
    return (a.join(b, condition).filter(F.col('a.x') <= F.col('a.y'))
            .select('a.x', 'a.y').distinct().orderBy('x', 'y'))


def q03(t):
    e = t['edges'].filter(F.col('a') != F.col('b'))
    directed = (e.select(F.col('a').alias('id'), F.col('b').alias('neighbor'))
                .union(e.select('b', 'a')).distinct())
    return (t['people'].join(directed, 'id', 'left').groupBy('id')
            .agg(F.count('neighbor').alias('neighbors')).orderBy('id'))


def q04(t):
    e = (t['edges'].filter(F.col('src') != F.col('dst'))
         .select(F.least('src', 'dst').alias('a'), F.greatest('src', 'dst').alias('b')).distinct())
    paths = (e.alias('x').join(e.alias('y'), F.col('x.b') == F.col('y.a'))
             .select('x.a', 'x.b', F.col('y.b').alias('c')))
    return (paths.alias('p').join(e.alias('z'),
            (F.col('p.a') == F.col('z.a')) & (F.col('p.c') == F.col('z.b')), 'left_semi')
            .orderBy('a', 'b', 'c'))


def q05(t):
    e = t['edges'].select(F.col('a').alias('src'), F.col('b').alias('dst'))
    undirected = e.union(e.select(F.col('dst').alias('src'), F.col('src').alias('dst')))
    seeds = t['nodes'].select(F.col('id').alias('root'), F.col('id').alias('node'))
    return (reachability(seeds, undirected).groupBy('node')
            .agg(F.min('root').alias('component')).orderBy('node'))


def q06(t):
    d = t['observations'].distinct()
    g = d.withColumn('_island', F.col('value') - F.row_number().over(Window.orderBy('value')))
    return (g.groupBy('_island').agg(F.min('value').alias('start_value'),
            F.max('value').alias('end_value'), F.count('*').alias('length'))
            .drop('_island').orderBy('start_value'))


def q07(t):
    w = Window.partitionBy('user_id').orderBy('day_no')
    g = t['logins'].distinct().withColumn('_island', F.col('day_no') - F.row_number().over(w))
    streaks = g.groupBy('user_id', '_island').agg(F.min('day_no').alias('start_day'),
        F.max('day_no').alias('end_day'), F.count('*').alias('days'))
    return (streaks.withColumn('_longest', F.max('days').over(Window.partitionBy('user_id')))
            .filter(F.col('days') == F.col('_longest'))
            .select('user_id', 'start_day', 'end_day', 'days').orderBy('user_id', 'start_day'))


def q08(t):
    spark = t['ids'].sparkSession
    points = t['ids'].union(spark.createDataFrame([(0,), (13,)], 'id long')).distinct()
    gaps = points.withColumn('_next', F.lead('id').over(Window.orderBy('id')))
    return (gaps.filter(F.col('_next') > F.col('id') + 1)
            .select((F.col('id') + 1).alias('gap_start'), (F.col('_next') - 1).alias('gap_end'))
            .orderBy('gap_start'))


def q09(t):
    w = Window.partitionBy('user_id').orderBy('minute_no', 'event_id')
    p = t['events'].withColumn('_prev', F.lag('minute_no').over(w))
    f = p.withColumn('_fresh', F.when(F.col('_prev').isNull() |
        (F.col('minute_no') - F.col('_prev') > 30), 1).otherwise(0))
    return (f.withColumn('session_no', F.sum('_fresh').over(prefix(w)))
            .groupBy('user_id', 'session_no').agg(F.min('minute_no').alias('start_minute'),
                F.max('minute_no').alias('end_minute'), F.count('*').alias('events'))
            .orderBy('user_id', 'session_no'))


def q10(t):
    w = Window.orderBy('day_no')
    p = (t['daily'].withColumn('_prev_day', F.lag('day_no').over(w))
         .withColumn('_prev_status', F.lag('status').over(w)))
    same_run = (F.col('day_no') == F.col('_prev_day') + 1) & F.col('status').eqNullSafe(F.col('_prev_status'))
    f = p.withColumn('_fresh', F.when(same_run, 0).otherwise(1))
    return (f.withColumn('_island', F.sum('_fresh').over(prefix(w)))
            .groupBy('_island', 'status').agg(F.min('day_no').alias('start_day'), F.max('day_no').alias('end_day'))
            .select('status', 'start_day', 'end_day').orderBy('start_day'))


def q11(t):
    g = (t['visits'].filter(F.col('people') >= 100)
         .withColumn('_island', F.col('id') - F.row_number().over(Window.orderBy('id'))))
    return (g.withColumn('_length', F.count('*').over(Window.partitionBy('_island')))
            .filter('_length >= 3').select('id', 'day_no', 'people').orderBy('id'))


def q12(t):
    g = t['tasks'].withColumn('_island', F.col('start_day') - F.row_number().over(Window.orderBy('start_day')))
    return (g.groupBy('_island').agg(F.min('start_day').alias('project_start'), F.max('end_day').alias('project_end'))
            .withColumn('duration', F.col('project_end') - F.col('project_start'))
            .drop('_island').orderBy('duration', 'project_start'))


def q13(t):
    return pack_intervals(t['intervals']).orderBy('start_at')


def q14(t):
    packed = pack_intervals(t['bookings'])
    padding = packed.sparkSession.createDataFrame([(0, 0), (20, 20)], 'start_at long, end_at long')
    gaps = packed.union(padding).withColumn('free_end', F.lead('start_at').over(Window.orderBy('start_at', 'end_at')))
    return (gaps.filter(F.col('free_end') > F.col('end_at'))
            .select(F.col('end_at').alias('free_start'), 'free_end').orderBy('free_start'))


def q15(t):
    m = t['meetings']
    events = (m.select(F.col('start_at').alias('at'), F.lit(1).alias('delta'))
              .union(m.select(F.col('end_at').alias('at'), F.lit(-1).alias('delta'))))
    w = Window.orderBy('at')
    segments = (events.groupBy('at').agg(F.sum('delta').alias('delta'))
                .withColumn('until', F.lead('at').over(w))
                .withColumn('active', F.sum('delta').over(prefix(w)))
                .filter(F.col('until') > F.col('at')))
    return (segments.withColumn('_peak', F.max('active').over(Window.partitionBy()))
            .filter(F.col('active') == F.col('_peak'))
            .select(F.col('at').alias('start_at'), F.col('until').alias('end_at'), 'active').orderBy('start_at'))


def q16(t):
    return pack_intervals(t['ranges'], 's', 'e').agg(
        F.coalesce(F.sum(F.col('e') - F.col('s')), F.lit(0)).alias('occupied'))


def q17(t):
    latest = (t['changes'].filter('day_no <= 5').withColumn('_rn',
              F.row_number().over(Window.partitionBy('product_id').orderBy(F.desc('day_no'))))
              .filter('_rn = 1').select(F.col('product_id').alias('id'), 'price'))
    return t['products'].join(latest, 'id', 'left').fillna({'price': 10}).orderBy('id')


def q18(t):
    f, v = t['facts'].alias('f'), t['versions'].alias('v')
    condition = ((F.col('f.key_id') == F.col('v.key_id')) & (F.col('f.at') >= F.col('v.valid_from')) &
                 ((F.col('f.at') < F.col('v.valid_to')) | F.col('v.valid_to').isNull()))
    return f.join(v, condition, 'left').select('f.id', 'v.label').orderBy('id')


def q19(t):
    candidates = (t['targets'].alias('t').crossJoin(t['readings'].alias('r'))
        .select(F.col('t.id').alias('target_id'), F.col('r.id').alias('reading_id'), 'r.value',
                F.col('r.at').alias('_reading_at'), F.abs(F.col('t.at') - F.col('r.at')).alias('_distance')))
    w = Window.partitionBy('target_id').orderBy('_distance', '_reading_at', 'reading_id')
    return (candidates.withColumn('_rn', F.row_number().over(w)).filter('_rn = 1')
            .select('target_id', 'reading_id', 'value').orderBy('target_id'))


def q20(t):
    buyers = t['purchases'].select(F.col('customer_id').alias('id'))
    return t['customers'].join(buyers, 'id', 'left_anti').orderBy('id')


def q21(t):
    paid = (t['orders'].filter(F.col('status') == 'paid').groupBy('customer_id')
            .agg(F.count('*').alias('paid_orders')).withColumnRenamed('customer_id', 'id'))
    return t['customers'].join(paid, 'id', 'left').fillna({'paid_orders': 0}).orderBy('id')


def q22(t):
    o = t['orders'].groupBy('customer_id').agg(F.sum('amount').alias('ordered')).withColumnRenamed('customer_id', 'id')
    p = t['payments'].groupBy('customer_id').agg(F.sum('amount').alias('paid')).withColumnRenamed('customer_id', 'id')
    return (t['customers'].join(o, 'id', 'left').join(p, 'id', 'left')
            .fillna({'ordered': 0, 'paid': 0}).orderBy('id'))


def q23(t):
    approved = t['tags'].filter(F.col('tag') == 'approved').select(F.col('invoice_id').alias('id'))
    return t['invoices'].join(approved, 'id', 'left_semi').agg(
        F.coalesce(F.sum('amount'), F.lit(0)).alias('approved_total'))


def q24(t):
    o, n = t['old_snapshot'].alias('o'), t['new_snapshot'].alias('n')
    joined = o.join(n, F.col('o.id') == F.col('n.id'), 'full')
    return (joined.filter(F.col('o.id').isNull() | F.col('n.id').isNull() |
                          ~F.col('o.val').eqNullSafe(F.col('n.val')))
            .select(F.coalesce('o.id', 'n.id').alias('id'),
                F.when(F.col('o.id').isNull(), 'added').when(F.col('n.id').isNull(), 'removed')
                    .otherwise('changed').alias('change_kind'),
                F.col('o.val').alias('old_value'), F.col('n.val').alias('new_value')).orderBy('id'))


def q25(t):
    signed = t['old_bag'].withColumn('delta', F.lit(-1)).unionByName(t['new_bag'].withColumn('delta', F.lit(1)))
    return (signed.groupBy('key_name').agg(F.sum('delta').alias('delta'))
            .filter('delta <> 0').orderBy(F.col('key_name').asc_nulls_first()))


def q26(t):
    # An anti join finds each missing customer/product pair; another excludes its customer.
    wanted = t['customers'].crossJoin(t['required'])
    bought = t['purchases'].select(F.col('customer_id').alias('id'), 'product').distinct()
    missing = wanted.join(bought, ['id', 'product'], 'left_anti').select('id').distinct()
    return t['customers'].join(missing, 'id', 'left_anti').orderBy('id')


def q27(t):
    covered = q26(t)
    extra = (t['purchases'].join(t['required'], 'product', 'left_anti')
             .select(F.col('customer_id').alias('id')).distinct())
    return covered.join(extra, 'id', 'left_anti').orderBy('id')


def q28(t):
    # collect_set is a per-customer executor aggregation, not DataFrame.collect().
    baskets = (t['basket'].groupBy('customer_id').agg(F.sort_array(F.collect_set('product')).alias('_basket'))
               .withColumnRenamed('customer_id', 'id'))
    empty = F.array().cast('array<string>')
    customers = t['customers'].join(baskets, 'id', 'left').withColumn('_basket', F.coalesce('_basket', empty))
    return (customers.alias('a').join(customers.alias('b'),
            (F.col('a.id') < F.col('b.id')) & (F.col('a._basket') == F.col('b._basket')))
            .select(F.col('a.id').alias('a'), F.col('b.id').alias('b')).orderBy('a', 'b'))


def q29(t):
    w = Window.partitionBy('exam_id')
    scores = t['scores'].withColumn('_lo', F.min('score').over(w)).withColumn('_hi', F.max('score').over(w))
    taken = scores.select(F.col('student_id').alias('id'))
    extreme = scores.filter((F.col('score') == F.col('_lo')) | (F.col('score') == F.col('_hi'))).select(F.col('student_id').alias('id'))
    return t['students'].join(taken, 'id', 'left_semi').join(extreme, 'id', 'left_anti').orderBy('id')


def q30(t):
    flags = (t['policies'].withColumn('_prior_count', F.count('*').over(Window.partitionBy('prior_value')))
             .withColumn('_location_count', F.count('*').over(Window.partitionBy('lat', 'lon'))))
    return flags.filter('_prior_count > 1 AND _location_count = 1').agg(
        F.coalesce(F.sum('current_value'), F.lit(0)).alias('total'))


def q31(t):
    rows = prefix(Window.orderBy('at', 'id'))
    peers = Window.orderBy('at').rangeBetween(Window.unboundedPreceding, Window.currentRow)
    return (t['tx'].withColumn('row_total', F.sum('amount').over(rows))
            .withColumn('peer_total', F.sum('amount').over(peers)).orderBy('at', 'id')
            .select('id', 'row_total', 'peer_total'))


def q32(t):
    w = Window.partitionBy('user_id').orderBy('at', 'id').rowsBetween(
        Window.unboundedPreceding, Window.unboundedFollowing)
    return t['events'].select('id', F.last('val', ignorenulls=False).over(w).alias('final_value')).orderBy('id')


def q33(t):
    w = prefix(Window.partitionBy('user_id').orderBy('at', 'id'))
    return t['readings'].select('id', F.last('val', ignorenulls=True).over(w).alias('filled_value')).orderBy('id')


def q34(t):
    calendar = t['sales'].sparkSession.range(1, 6).select(F.col('id').alias('day_no'))
    totals = t['sales'].groupBy('day_no').agg(F.sum('amount').alias('amount'))
    daily = calendar.join(totals, 'day_no', 'left').fillna({'amount': 0})
    rolled = daily.withColumn('window_total', F.sum('amount').over(Window.orderBy('day_no').rowsBetween(-2, 0)))
    return (rolled.filter('day_no >= 3').select('day_no', 'window_total',
            F.round(F.col('window_total') / 3.0, 2).alias('average')).orderBy('day_no'))


def q35(t):
    c, a = t['calendar'].alias('c'), t['activity'].alias('a')
    condition = (F.col('a.day_no') >= F.col('c.day_no') - 2) & (F.col('a.day_no') <= F.col('c.day_no'))
    return (c.join(a, condition, 'left').groupBy('c.day_no')
            .agg(F.countDistinct('a.user_id').alias('active_users')).orderBy('day_no'))


def q36(t):
    first = t['events'].withColumn('_occurrence', F.row_number().over(Window.partitionBy('user_id').orderBy('at', 'id')))
    marker = F.when(F.col('user_id').isNotNull() & (F.col('_occurrence') == 1), 1).otherwise(0)
    return (first.withColumn('distinct_users', F.sum(marker).over(prefix(Window.orderBy('at', 'id'))))
            .orderBy('at', 'id').select('id', 'distinct_users'))


def q37(t):
    ordered = (t['employees'].withColumn('_rn', F.row_number().over(Window.partitionBy('company').orderBy('salary', 'id')))
               .withColumn('_n', F.count('*').over(Window.partitionBy('company'))))
    middle = ordered.filter((F.col('_rn') >= F.floor((F.col('_n') + 1) / 2)) &
                            (F.col('_rn') <= F.floor((F.col('_n') + 2) / 2)))
    return middle.groupBy('company').agg(F.avg('salary').alias('median')).orderBy('company')


def q38(t):
    f = t['frequencies']
    bounds = f.withColumn('_hi', F.sum('freq').over(prefix(Window.orderBy('val'))))
    n = f.agg(F.sum('freq').alias('_n'))
    # explode an array of TWO positions only. Repeated middle positions must stay.
    positions = n.select(F.explode(F.array(F.expr('(_n DIV 2) + (_n % 2)'),
                                          F.expr('(_n DIV 2) + 1'))).alias('_p'))
    condition = (F.col('_p') > F.col('_hi') - F.col('freq')) & (F.col('_p') <= F.col('_hi'))
    return positions.join(bounds, condition).agg(F.avg('val').alias('median'))


def q39(t):
    totals = t['queue'].withColumn('_total', F.sum('weight').over(prefix(Window.orderBy('turn'))))
    return totals.filter('_total <= 1000').orderBy(F.desc('turn')).limit(1).select('turn', 'name')


def q40(t):
    grouped = t['events'].withColumn('_grp', F.sum('is_reset').over(prefix(Window.orderBy('seq'))))
    w = prefix(Window.partitionBy('_grp').orderBy('seq'))
    return grouped.select('seq', F.sum('amount').over(w).alias('running_total')).orderBy('seq')


def q41(t):
    w = Window.orderBy('seq')
    adjacent = t['logs'].withColumn('_next', F.lead('val', 1).over(w)).withColumn('_next2', F.lead('val', 2).over(w))
    return (adjacent.filter((F.col('val') == F.col('_next')) & (F.col('val') == F.col('_next2')))
            .select('val').distinct().orderBy('val'))


def q42(t):
    w = Window.orderBy('seat_id')
    seats = (t['seats'].withColumn('_pos', F.row_number().over(w))
             .withColumn('_next', F.lead('occupant').over(w)).withColumn('_prev', F.lag('occupant').over(w)))
    return seats.select('seat_id', F.when(F.col('_pos') % 2 == 1,
        F.coalesce('_next', 'occupant')).otherwise(F.col('_prev')).alias('occupant')).orderBy('seat_id')


def q43(t):
    m = t['matches']
    points = (m.select(F.col('first_player').alias('id'), F.col('first_score').alias('score'))
              .union(m.select('second_player', 'second_score')))
    totals = points.groupBy('id').agg(F.sum('score').alias('score'))
    players = t['players'].join(totals, 'id', 'left').fillna({'score': 0})
    w = Window.partitionBy('group_id').orderBy(F.desc('score'), 'id')
    return (players.withColumn('_rn', F.row_number().over(w)).filter('_rn = 1')
            .select('group_id', F.col('id').alias('winner_id'), 'score').orderBy('group_id'))


def q44(t):
    u, a = t['users'].alias('u'), t['activity'].distinct().alias('a')
    condition = (F.col('u.id') == F.col('a.user_id')) & (F.col('a.day_no') == F.col('u.signup_day') + 1)
    return (u.join(a, condition, 'left').groupBy('u.signup_day')
            .agg(F.round(F.avg(F.when(F.col('a.user_id').isNotNull(), 1.0).otherwise(0.0)), 2).alias('retention'))
            .orderBy('signup_day'))


def q45(t):
    monthly = t['credits'].groupBy('account_id', 'month_index').agg(F.sum('amount').alias('_total'))
    limits = t['accounts'].select(F.col('id').alias('account_id'), 'monthly_limit')
    over = monthly.join(limits, 'account_id').filter(F.col('_total') > F.col('monthly_limit'))
    adjacent = over.withColumn('_prev', F.lag('month_index').over(Window.partitionBy('account_id').orderBy('month_index')))
    return adjacent.filter(F.col('month_index') == F.col('_prev') + 1).select('account_id').distinct().orderBy('account_id')


def q46(t):
    edges = t['reports'].select(F.col('manager_id').alias('src'), F.col('employee_id').alias('dst'))
    seed = edges.sparkSession.createDataFrame([(1, 1)], 'root long, node long')
    return reachability(seed, edges).filter('node <> 1').select(F.col('node').alias('id')).orderBy('id')


def q47(t):
    parents = t['nodes'].select(F.col('parent_id').alias('id')).filter('id IS NOT NULL').distinct().withColumn('_has_child', F.lit(True))
    return (t['nodes'].join(parents, 'id', 'left').select('id',
            F.when(F.col('parent_id').isNull(), 'Root').when(F.col('_has_child'), 'Inner')
                .otherwise('Leaf').alias('node_type')).orderBy('id'))


def q48(t):
    e = t['events']
    first_view = e.filter(F.col('kind') == 'view').groupBy('user_id').agg(F.min('at').alias('_view'))
    first_add = (e.filter(F.col('kind') == 'add').join(first_view, 'user_id')
                 .filter(F.col('at') > F.col('_view')).groupBy('user_id').agg(F.min('at').alias('_add')))
    return (e.filter(F.col('kind') == 'buy').join(first_add, 'user_id').filter(F.col('at') > F.col('_add'))
            .select('user_id').distinct().orderBy('user_id'))


def q49(t):
    w = prefix(Window.orderBy('id'))
    s = t['supplies'].withColumn('hi', F.sum('qty').over(w)).alias('s')
    d = t['demands'].withColumn('hi', F.sum('qty').over(w)).alias('d')
    lo = F.greatest(F.col('s.hi') - F.col('s.qty'), F.col('d.hi') - F.col('d.qty'))
    hi = F.least('s.hi', 'd.hi')
    return (s.join(d, hi > lo).select(F.col('d.id').alias('demand_id'), F.col('s.id').alias('supply_id'),
            (hi - lo).alias('allocated')).orderBy('demand_id', 'supply_id'))


def q50(t):
    m = t['movements']
    receipts = m.filter(F.col('kind') == 'IN').withColumn('_hi', F.sum('qty').over(prefix(Window.partitionBy('product').orderBy('id'))))
    sold = m.groupBy('product').agg(F.sum(F.when(F.col('kind') == 'OUT', F.col('qty')).otherwise(0)).alias('_sold'))
    remaining = receipts.join(sold, 'product').withColumn('_remaining',
        F.greatest(F.lit(0), F.least(F.col('qty'), F.col('_hi') - F.col('_sold'))))
    return (remaining.groupBy('product').agg(F.sum('_remaining').alias('remaining_qty'),
            F.sum(F.col('_remaining') * F.col('cost')).alias('inventory_value')).orderBy('product'))


SOLUTIONS = {f'Q{i:02d}': globals()[f'q{i:02d}'] for i in range(1, 51)}
