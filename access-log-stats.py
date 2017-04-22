class Series:
    def __init__(self):
        self.items = {}
        self.stat_cache = [0, -1, -1, -1, -1, -1]
        self.stat_cache_invalid = False

    def add_one(self, time):
        self.add(time, 1)

    def add(self, time, count):
        i = self.items.get(time)
        if i is None:
            self.items[time] = count
        else:
            self.items[time] = i + count
        self.stat_cache_invalid = True

    def count(self):
        if not self.stat_cache_invalid:
            return self.stat_cache[0]
        c = 0
        for time, count in self.items.items():
            c += count
        return c

    def average(self):
        if not self.stat_cache_invalid:
            return self.stat_cache[1]
        c = 0
        t = 0
        for time, count in self.items.items():
            c += count
            t += time * count
        return t / c

    def stats(self):
        if not self.stat_cache_invalid:
            return self.stat_cache
        a = self.items.items()
        a.sort()
        n = self.count()
        acc = 0
        avg = 0
        result = [n,-1,-1,-1,-1,-1]  # count, avg, 75p, 90p, 95p, 99p
        for t,c in a:
            acc += c
            if result[2] == -1 and acc >= n*0.75:
                result[2] = t
            if result[3] == -1 and acc >= n*0.9:
                result[3] = t
            if result[4] == -1 and acc >= n*0.95:
                result[4] = t
            if result[5] == -1 and acc >= n*0.99:
                result[5] = t
            avg += t * c
        if acc != 0: result[1] = avg / acc
        self.stat_cache = result
        self.stat_cache_invalid = False
        return result

import sys
import urlparse
import re

html = []

def stat_output(result):
    url_count = 0
    for response, series in result.items():
        url_count += series.count()
    stat = [url_count, -1, -1, -1, -1, -1]
    if 200 in result:
        stat = result[200].stats()
    return stat

def simple_output(result):
    stat = stat_output(result)
    return '{0:7d} {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.3f}'.format(*stat)

def html_output(result):
    stat = stat_output(result)
    return "<td>{0:d}</td><td>{1:.3f}</td><td>{2:.3f}</td><td>{3:.3f}</td><td>{4:.3f}</td><td>{5:.3f}</td>".format(*stat)


def print_volume_top(stats, N):
    # access count top N
    sort_array = []
    total_c = 0
    for url, result in url_stats.items():
        url_count = 0
        for response, series in result.items():
            url_count += series.count()
        total_c += url_count
        sort_array.append((url_count, url))
    sort_array.sort(key=lambda x:x[0], reverse=True)
    html.append("<h1>Volume Top %d</h1>"%N)
    html.append("""\
<table>
	<thead>
	  <tr>
	  	<th>Method</th>
	  	<th>URL</th>
	  	<th>Volume</th>
	  	<th>2xx Volume</th>
	  	<th>Avg</th>
	  	<th>70p</th>
	  	<th>90p</th>
	  	<th>95p</th>
	  	<th>99p</th>
	  </tr>
	</thead>
	<tbody>""")
    #print "\n========== volume top %d =========="%N
    for (count, url) in sort_array[:N]:
        #print "{0:<4s} {1:<50s} {2:7d} {3:s}".format(url[0], url[1], count, simple_output(stats[url])) #, stats[url]
        html.append("<tr><td>{0:s}</td><td>{1:s}</td><td>{2:d}</td>{3:s}</tr>".format(url[0],url[1],count,html_output(stats[url])))
    html.append("</tbody></table>")


def print_slowest_top(stats, N):
    sort_array = []
    for url, result in url_stats.items():
        if 200 in result:
            sort_array.append((result[200].average(), url))
    sort_array.sort(key=lambda x:x[0], reverse=True)
    html.append("<h1>Slowest Top %d</h1>"%N)
    html.append("""\
<table>
	<thead>
	  <tr>
	  	<th>Method</th>
	  	<th>URL</th>
	  	<th>Avg</th>
	  	<th>2xx Volume</th>
	  	<th>Avg</th>
	  	<th>70p</th>
	  	<th>90p</th>
	  	<th>95p</th>
	  	<th>99p</th>
	  </tr>
	</thead>
	<tbody>""")
    #print "\n========== slowest top %d =========="%N
    for (count, url) in sort_array[:N]:
        #print "{0:<4s} {1:<50s} {2:7.3f} {3:s}".format(url[0], url[1], count, simple_output(stats[url])) #, stats[url]
        html.append("<tr><td>{0:s}</td><td>{1:s}</td><td>{2:.3f}</td>{3:s}</tr>".format(url[0],url[1],count,html_output(stats[url])))
    html.append("</tbody></table>")

def print_error_top(stats, N):
    sort_array = []
    for url, result in url_stats.items():
        wrong_count = 0
        right_count = 0
        for response, series in result.items():
            if 200 == response:
                right_count += series.count()
            else:
                wrong_count += series.count()
        if wrong_count + right_count > 100:  # set the threadshold
            sort_array.append((wrong_count/float(wrong_count+right_count), url))
    sort_array.sort(key=lambda x:x[0], reverse=True)
    html.append("<h1>Error Rate Top %d</h1>"%N)
    html.append("""\
<table>
	<thead>
	  <tr>
	  	<th>Method</th>
	  	<th>URL</th>
	  	<th>Error Rate</th>
	  	<th>2xx Volume</th>
	  	<th>Avg</th>
	  	<th>70p</th>
	  	<th>90p</th>
	  	<th>95p</th>
	  	<th>99p</th>
	  </tr>
	</thead>
	<tbody>""")
    #print "\n========== error rate top %d =========="%N
    for (error_rate, url) in sort_array[:N]:
        #print "{0:<4s} {1:<50s} {2:6.2f}% {3:s}".format(url[0], url[1], error_rate*100, simple_output(stats[url])) #, stats[url]
        html.append("<tr><td>{0:s}</td><td>{1:s}</td><td>{2:.2f}%</td>{3:s}</tr>".format(url[0],url[1],error_rate*100,html_output(stats[url])))
    html.append("</tbody></table>")

def print_stats(stats):
    N = 15
    html.append("""
<html>
<head>
    <style>

body{
	width:64%;
}
      
h1{
  font-size: 30px;
  color: #000;
  text-transform: uppercase;
  font-weight: 300;
  text-align: center;
  margin-bottom: 15px;
}
table{
  width:100%;
}
th{
  padding: 5px;
  text-align: left;
  font-weight: 500;
  font-size: 14px;
  color: #000;
  text-transform: uppercase;
  border-bottom: solid 1px rgba(0,0,0,0.2);
}
td{
  padding: 5px;
  text-align: left;
  vertical-align:middle;
  font-weight: 300;
  font-size: 14px;
  color: #000;
  border-bottom: solid 1px rgba(0,0,0,0.1);
}

    </style>
</head>
<body>""")
    print_volume_top(stats, N)
    print_slowest_top(stats, N)
    print_error_top(stats, N)
    html.append("""
</body>
</html>""")
    #file("hoho.html","w").write("\n".join(html))
    print "\n".join(html)

url_map = [
    (re.compile('/cms/program_detail/recommend_byvod/\d+'), '/cms/program_detail/recommend_byvod/{ID}'),
    (re.compile('/cms/program_detail/recommend/-?\d+'), '/cms/program_detail/recommend/{ID}'),
    (re.compile('/cms/program_detail/\d+'), '/cms/program_detail/{ID}'),
    (re.compile('/cms/program_detail/video/\d+'), '/cms/program_detail/video/{ID}'),
    (re.compile('/cms/program_detail/byvod/\d+'), '/cms/program_detail/byvod/{ID}'),
    (re.compile('/cms/channels/-?\d+/historyChats'), '/cms/channels/{ID}/historyChats'),
    (re.compile('/cms/channels/-?\d+/chartsOnline'), '/cms/channels/{ID}/chartsOnline'),
    (re.compile('/cms/channels/\d+'), '/cms/channels/{ID}'),
    (re.compile('/cms/channels/-?\d+/charts/text'), '/cms/channels/{ID}/charts/text'),
    (re.compile('/cms/channels/-?\d+/charts/image'), '/cms/channels/{ID}/charts/image'),
    (re.compile('/cms/channels/comments/\d+'), '/cms/channels/comments/{ID}'),
    (re.compile('/cms/chatroom/\d+/notification'), '/cms/chatroom/{ID}/notification'),
    (re.compile('/cms/chatroom/\d+/alert'), '/cms/chatroom/{ID}/alert'),
    (re.compile('/cms/sections/\d+'), '/cms/sections/{ID}'),
    (re.compile('/cms/soccer/matches/\d+'), '/cms/soccer/matches/{ID}'),
    (re.compile('/cms/soccer/ranking/\d+'), '/cms/soccer/ranking/{ID}'),
    (re.compile('/cms/programs/\d+'), '/cms/programs/{ID}'),
    (re.compile('/cms/programs/\d+/comments'), '/cms/programs/{ID}/comments'),
    (re.compile('/cms/vods/\d+'), '/cms/vods/{ID}'),
    (re.compile('/cms/vod/\d+/channel'), '/cms/vod/{ID}/channel'),
    (re.compile('/cms/sms/bindcard/order/\d+'), '/cms/sms/bindcard/order/{ID}'),
    (re.compile('/cms/sms/recharge/order/\d+'), '/cms/sms/recharge/order/{ID}'),
    (re.compile('/cms/sms/changepackage/order/\d+'), '/cms/sms/changepackage/order/{ID}'),
    (re.compile('/cms/tasks/\d+'), '/cms/tasks/{ID}'),
    (re.compile('/cms/user/smartCardInfo/\d+'), '/cms/user/smartCardInfo/{ID}'),
    (re.compile('/bbs/posts/list/\d+/50.page'), '/bbs/posts/list/{ID}/50.page'),
    (re.compile('/bbs/posts/list/\d+.page'), '/bbs/posts/list/{ID}.page'),
    (re.compile('/portal/img/.*'), '/portal/img/{PATH}'),

    # bossproxy pattern map
    (re.compile('/customers/(.*?)/\d+/book_balance'), '/customers/{cusId}/book_balance'),
    (re.compile('/customers/(.*?)/\d+/bills'), '/customers/{cusId}/bills'),
    (re.compile('/customers/(.*?)/\d+/payments2'), '/customers/{cusId}/payments2'),
    (re.compile('/customers/(.*?)/\d+/subscribers'), '/customers/{cusId}/subscribers'),
    (re.compile('/smartcards/(.*?)/\d+/subscribers'), '/smartcards/{smartCardNo}/subscribers'),
    (re.compile('/smartcards/(.*?)/\d+/products'), '/smartcards/{smartCardNo}/products'),
    (re.compile('/smartcards/(.*?)/\d+/expected_stop_date'), '/smartcards/{smartCardNo}/expected_stop_date'),
    (re.compile('/smartcards/(.*?)/\d+/recharge'), '/smartcards/{smartCardNo}/recharge'),
    (re.compile('/smartcards/(.*?)/\d+/change_product'), '/smartcards/{smartCardNo}/change_product'),
    (re.compile('/smartcards/(.*?)/\d+/recharge_by_wallet'), '/smartcards/{smartCardNo}/recharge_by_wallet'),
  #  (re.compile(''), ''),
    ]
def map_url_pattern(url):
    for r, v in url_map:
        token = r.match(url)
        if token is not None:
            fields = token.groups()
            if len(fields) > 0:
                return "/" + fields[0] + v
            return v
    return url

if __name__ == '__main__':
    url_stats = {}
    log_re = re.compile('^(.*?) (.*?) ([(\d\.)]+) - - \[(.*?)\] "(.*?) (.*?) (.*?)" (\d+) (\d+) ".*" "(.*?)" (.*?) (.*?)$')
    for line in sys.stdin:
        token = log_re.match(line)
        if token is not None:
            fields = token.groups()
            method = fields[4]
            raw_url = fields[5]
            url = urlparse.urlparse(raw_url)
            url_pattern = map_url_pattern(url.path)

            # handle query country
            if "country" == url.query[:7]:
                url_pattern = "/" + url.query[8:10] + url_pattern

            response = int(fields[7])/100*100 # 2xx,3xx,4xx,5xx
            elasped = float(fields[11])
            url_result = url_stats.get((method, url_pattern))
            if url_result is None:
                url_result = {}
                url_stats[(method, url_pattern)] = url_result
            url_series = url_result.get(response)
            if url_series is None:
                url_series = Series()
                url_result[response] = url_series
            url_series.add_one(elasped)
        else:
            #print line
            pass

    print_stats(url_stats)

        
