import time
import re
import json
import csv
import datetime
import jinja2
import matplotlib.pyplot as plt
from http.server import HTTPServer, BaseHTTPRequestHandler
from functools import partial
import urllib.parse as urlparser
from qbstyles import mpl_style

from gameoflife import create_initial_grid, create_next_grid


HOST_NAME = 'localhost'
PORT_NUMBER = 8081

LINE_LENGTH = 25

SLIDE_SECONDS = 15

DORMS = [
    "Charollais",
    "Primera",
    "Merino",
    "Masham",
    "Beltex",
    "Dorper",
    "Llanwenog",
    "Meatlinc",
    "Lonk",
    "Zwartbles",
    "Torwen Badger-Face",
]

def line_span(a, b):
    return a + b.rjust(LINE_LENGTH - len(a))

class AbstractSlide:
    def __init__(self):
        self.slide_time = SLIDE_SECONDS

    def get_text(self):
        return NotImplementedError

    def render_lines(self, lines):
        s = f"<h2>{lines.pop(0)}</h2>"
        for line in lines:
            s += f"<h3>{line}</h3>"

        return s

    def can_display(self):
        return True

class GameOfLifeSlide(AbstractSlide):
    def __init__(self):
        super().__init__()
        self.grid = create_initial_grid(40, 100)
        self.last_update = time.time_ns()

    def render_grid(self):
        s = ""
        for row in self.grid:
            for cell in row:
                if cell:
                    s += '█'
                else:
                    s += '&nbsp;'
            s += "<br>"
        return s

    def get_text(self):
        if time.time_ns() > self.last_update + 30 * 1000 * 1000 * 1000:
            new_grid = create_initial_grid(40, 100)
            create_next_grid(40, 100, self.grid, new_grid)
            self.grid = new_grid
            self.last_update = time.time_ns()

        return '<div class="gol">{}<br>hello</div>'.format(self.render_grid())


class ScoreSlide(AbstractSlide):
    def __init__(self, sort=False):
        super().__init__()
        self.slide_time = 30
        self._sort = sort
        # Read scores from file
        scores_dict = {}
        for i in DORMS:
            scores_dict[i] = 0
        with open("scores.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    scores_dict[row[0]] = scores_dict.get(row[0], 0) + int(row[1])
                except Exception:
                    pass

        if self._sort:
            self.scores = [i for i in sorted(scores_dict.items(), key=lambda item: item[1])]
        else:
            self.scores = [i for i in scores_dict.items()]

        self.generate_bar_chart()

    def generate_bar_chart(self):
        dorms = [i[0] for i in self.scores]
        points = [i[1] for i in self.scores]
        #mpl_style(dark=True)
        plt.style.use("dark_background")
        fig, ax = plt.subplots()
        ypos = [i*0.5 for i in range(len(self.scores))]
        ax.barh(ypos, points, height=0.3)
        ax.set_yticks(ypos, labels=dorms)
        ax.invert_yaxis()
        ax.axvline(x=0, color='white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
        ax.patch.set_alpha(0.)
        fig.set_size_inches(5,3)
        fig.tight_layout()
        fig.patch.set_alpha(0.)
        fig.savefig("assets/dorm-points.svg")
        self.last_barchart = time.time_ns()

    def get_text(self):
        return self.render_lines(["Dorm points", '<img src="assets/dorm-points.svg?{}">'.format(self.last_barchart)])
        return self.get_html()
        lines = ["Dorm points", "",]
        for score in self.scores:
            lines.append(line_span(score[0], str(score[1])))
        return self.render_lines(lines)

    def get_html(self):
        text = "<h2>Dorm Points</h2><table>"
        for score in self.scores:
            text += "<tr><td>{}</td><td>{}</td></tr>".format(*score)
        text += "</table>"
        return text


class TimedSlide(AbstractSlide):
    def __init__(self, d):
        super().__init__()
        self.start_time = datetime.datetime.strptime(d['start'], '%Y-%m-%d %H:%M')
        self.end_time = datetime.datetime.strptime(d['end'], '%Y-%m-%d %H:%M')
        self.text = d['message']

    def can_display(self):
        return self.start_time <= datetime.datetime.now() <= self.end_time

    def get_text(self):
        return self.render_lines(self.text.split("\n"))
        #return self.text


class TimetableSlide(AbstractSlide):
    def __init__(self):
        super().__init__()
        with open("lwtt-2025-1.1.txt", "r") as f:
            raw_tt = f.read()
        lines = raw_tt.split("\n")
        # Remove comment lines
        lines = [i.split("\t") for i in lines if not i.strip().startswith("%") and len(i.strip())]
        # Split into days
        days = []
        day = []
        for line in lines:
            if line[0] != "----":
                day.append(line)
            else:
                day = [i for i in day if "Y" in i[1]]
                days.append(day)
                day = []

        day = [i for i in day if "Y" in i[1]]
        days.append(day)
        days = days[1:]

        start_time = datetime.time(hour=7, minute=0)
        # Timetable starts on the Saturday
        start_day = datetime.date(year=2025, month=8, day=9)

        self.events = []
        tracked_datetime = datetime.datetime.combine(start_day, start_time)
        for day in days:
            for item in day:
                try:
                    self.events.append([tracked_datetime, item[3]])
                except IndexError:
                    pass
                m = 15 * int(item[0])
                delta = datetime.timedelta(hours=(m // 60), minutes=(m % 60))
                tracked_datetime += delta

            tracked_datetime = datetime.datetime.combine(tracked_datetime.date(), start_time)
            tracked_datetime += datetime.timedelta(days=1)

    def get_text(self):
        next_events = []
        for event in self.events:
            if event[0] > datetime.datetime.now():
                if event[0].date() == datetime.datetime.now().date():
                    next_events.append(event)

        if len(next_events) > 5:
            next_events = next_events[:5]

        lines = []
        lines.append("Timetable")
        lines.append("")
        for e in next_events:
            lines.append("{} - {}".format(e[0].time().strftime("%H:%M"), e[1]))

        return self.render_lines(lines)

class TextSlide(AbstractSlide):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def get_text(self):
        return self.render_lines(self.text.split("\n"))
        #return self.text


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, server, *args, **kwargs):
        self._server = server
        super().__init__(*args, **kwargs)

    def do_GET(self):
        url = urlparser.urlparse(self.path)
        params = dict(urlparser.parse_qsl(url.query))
        response, content_type, data = self._server.serve(url.path, params)
        self.send_response(response)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        url = urlparser.urlparse(self.path)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        response, content_type, data = self._server.serve(url.path, post_body)
        self.send_response(response)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(data)


class Server:
    def __init__(self):
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
        self._urls = [
            (r'^/display/?$', self.show_display_page),
            (r'^/admin/?$', self.show_admin_page),
            (r'^/update/?$', self.get_data_update),
            (r'^/score$', self.update_score),
            (r'^/updatetext$', self.update_custom_slides),
            (r'^/assets/.*', self.serve_asset),
        ]
        self._timetable_slide = None
        #self._game_of_life_slide = GameOfLifeSlide()
        self.last_update = datetime.datetime.now()
        self.slide_index = 0
        self._reload_slides()

    def _reload_slides(self):
        self._score_slide = ScoreSlide()
        if self._timetable_slide is None:
            self._timetable_slide = TimetableSlide()

        with open("textslides.txt", "r") as f:
            self.raw_textslides_text = f.read()
        textslides_text = self.raw_textslides_text.split("\n_\n")

        self._slides = [
            #self._game_of_life_slide,
            self._score_slide,
            self._timetable_slide,
        ]

        for i in textslides_text:
            self._slides.append(TextSlide(i))

        with open('timed-slides.json', 'r') as f:
            timed = json.load(f)

        for i in timed:
            self._slides.append(TimedSlide(i))

        self.slide_index = min(self.slide_index, len(self._slides))

    def serve_html_from_template(self, template_fname, context):
        template = self.jinja_env.get_template(template_fname)
        content = template.render(**context)
        return 200, "text/html", bytes(content, "utf-8")

    def serve_asset(self, path, params):
        if path.endswith("svg"):
            mimetype="image/svg+xml"
        else:
            mimetype="file"
        with open("." + path, "rb") as f:
            return 200, mimetype, f.read()

    def serve_html_file(self, fname):
        with open(fname, "rb") as f:
            return 200, "text/html", f.read()

    def serve(self, path, params):
        for url in self._urls:
            if re.fullmatch(url[0], path):
                return url[1](path, params)
        return 404, None, b""

    def show_display_page(self, path, params):
        return self.serve_html_file("display.html")

    def show_admin_page(self, path, params):
        context = {
            "current_points": self._score_slide.get_html(),
            "text_slide_contents": self.raw_textslides_text,
            "dorms": DORMS,
        }
        return self.serve_html_from_template("admin.html", context)

    def get_data_update(self, path, params):
        now = datetime.datetime.now()
        slide_seconds = self._slides[self.slide_index].slide_time
        slide_timedelta = datetime.timedelta(seconds=slide_seconds)
        if now > self.last_update + slide_timedelta:
            while True:
                self.slide_index = (self.slide_index + 1) % len(self._slides)
                if self._slides[self.slide_index].can_display():
                    break
            self.last_update = now
        slide = self._slides[self.slide_index]
        return 200, "application/json", bytes(json.dumps({"new_text": slide.get_text()}), "utf-8")

    def update_score(self, path, data):
        params = json.loads(data.decode("utf-8"))
        word = "added to" if int(params["points"]) >= 0 else "subtracted from"
        if int(params["points"]) != 0:
            with open("scores.csv", "a") as f:
                f.write("\n{},{}".format(params["dorm"], params["points"]))
        self._reload_slides()
        feedback = "{} points {} dorm {}<br><br>{}".format(params["points"], word, params["dorm"], self._score_slide.get_html())

        return 200, "application/json", bytes(json.dumps({"feedback": feedback}), "utf-8")

    def update_custom_slides(self, path, data):
        params = json.loads(data.decode("utf-8"))
        if "text" not in params:
            return 404, None, b""
        with open("textslides.txt", "w") as f:
            f.write(params["text"])
        self._reload_slides()
        return 200, "application/json", b""

if __name__ == '__main__':
    server = Server()
    handler = partial(MyHandler, server)
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), handler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
