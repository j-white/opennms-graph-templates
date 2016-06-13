from jinja2 import Template


def histogram(report, name, title, rrd_prefix,
              percentiles=None,
              palette=None):
    template = """
report.{{ report }}.name={{ name }}
report.{{ report }}.columns={% for percentile in percentiles %}{{ rrd_prefix }}{{ percentile }}{% if not loop.last %},{% endif %}{% endfor %}
report.{{ report }}.type=interfaceSnmp
report.{{ report }}.command=--title="{{ title }}" \\
 --vertical-label="Milliseconds" \\
{%- for percentile in percentiles %}
 DEF:{{ percentile }}th={rrd{{ loop.index }}}:{{ rrd_prefix }}{{ percentile }}:AVERAGE \\
{%- endfor %}
{%- for percentile in percentiles %}
{%- if loop.first %}
 AREA:{{ percentile }}th{{ palette[loop.index-1] }}:"{{ percentile }}th percentile" \\
{%- else %}
 STACK:{{ percentile }}th{{ palette[loop.index-1] }}:"{{ percentile }}th percentile" \\
{%- endif %}
 GPRINT:{{ percentile }}th:AVERAGE:" Avg \\\\: %8.2lf %s" \\
 GPRINT:{{ percentile }}th:MIN:" Min \\\\: %8.2lf %s" \\
 GPRINT:{{ percentile }}th:MAX:" Max \\\\: %8.2lf %s\\\\n"{% if not loop.last %}\\{% endif %}
{%- endfor %}"""
    context = {
        'report': report,
        'name':  name,
        'title': title,
        'rrd_prefix': rrd_prefix,
        'percentiles': [50, 75, 95, 98, 99, 999] if percentiles is None else percentiles,
        # See http://www.colourlovers.com/palette/1930/cheer_up_emo_kid
        'palette': ['#556270', '#4ECDC4', '#C7F464', '#FF6B6B', '#C44D58', '#542437'] if palette is None else palette
    }
    return Template(template).render(context)

def garbage_collector_collections(code, name, rrd_prefix):
    template = """
report.jvm.gc.{{ code }}.collections.name=JVM GarbageCollector: {{ name }} Collections
report.jvm.gc.{{ code }}.collections.columns={{ rrd_prefix }}CollCnt
report.jvm.gc.{{ code }}.collections.type=interfaceSnmp
report.jvm.gc.{{ code }}.collections.command=--title="JVM GarbageCollector: {{ name }} Collections" \\
 DEF:collCnt={rrd1}:{{ rrd_prefix }}CollCnt:AVERAGE \\
 LINE2:collCnt#0000ff:"Collections" \\
 GPRINT:collCnt:AVERAGE:" Avg \\\\: %8.2lf %s" \\
 GPRINT:collCnt:MIN:" Min \\\\: %8.2lf %s" \\
 GPRINT:collCnt:MAX:" Max \\\\: %8.2lf %s\\\\n" """
    context = {
        'code': code,
        'name': name,
        'rrd_prefix': rrd_prefix
    }
    return Template(template).render(context)


def garbage_collector_collection_time(code, name, rrd_prefix):
    template = """
report.jvm.gc.{{ code }}.collection.time.name=JVM GarbageCollector: {{ name }} Collection Time
report.jvm.gc.{{ code }}.collection.time.columns={{ rrd_prefix }}CollTime
report.jvm.gc.{{ code }}.collection.time.type=interfaceSnmp
report.jvm.gc.{{ code }}.collection.time.command=--title="JVM GarbageCollector: {{ name }} Collection Time" \\
 DEF:collTime={rrd1}:{{ rrd_prefix }}CollTime:AVERAGE \\
 LINE2:collTime#0000ff:"Collection Time" \\
 GPRINT:collTime:AVERAGE:" Avg \\\\: %8.2lf %s" \\
 GPRINT:collTime:MIN:" Min \\\\: %8.2lf %s" \\
 GPRINT:collTime:MAX:" Max \\\\: %8.2lf %s\\\\n" """
    context = {
        'code': code,
        'name': name,
        'rrd_prefix': rrd_prefix
    }
    return Template(template).render(context)

def generate_newts_related_histograms():
    print histogram('OpenNMS.Newts.Sample.Insert.Latency',
                    'Newts Sample Insert Latency',
                    'Newts: Sample Insert Latency',
                    'NewtsInsert')
    print histogram('OpenNMS.Newts.Sample.Select.Latency',
                    'Newts Sample Select Latency',
                    'Newts: Sample Select Latency',
                    'NewtsSmplSelct')
    print histogram('OpenNMS.Newts.Measurement.Select.Latency',
                    'Newts Measurement Select Latency',
                    'Newts: Measurement Select Latency',
                    'NewtsMeasSelct')
    print histogram('OpenNMS.Newts.Index.Update.Latency',
                    'Newts Index Update Latency',
                    'Newts: Index Update Latency',
                    'NewtsSearchUpd')
    print histogram('OpenNMS.Newts.Index.Delete.Latency',
                    'Newts Index Delete Latency',
                    'Newts: Index Delete Latency',
                    'NewtsSearchDel')
    print histogram('OpenNMS.Cassanra.Cluster1.Request.Latency',
                    'Cassandra Cluster1 Request Latency',
                    'Cassandra: Request Latency',
                    'CasCluster1Req')

def generate_g1gc_stats():
    print garbage_collector_collections('g1young', 'G1 Young Generation', 'G1Yng')
    print garbage_collector_collection_time('g1young', 'G1 Young Generation', 'G1Yng')
    print garbage_collector_collections('g1old', 'G1 Old Generation', 'G1Old')
    print garbage_collector_collection_time('g1old', 'G1 Old Generation', 'G1Old')

if __name__ == "__main__":
    # generate_g1gc_stats()
    generate_newts_related_histograms()


