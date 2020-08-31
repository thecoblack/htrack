import datetime
import click
import os

from omegaconf import OmegaConf, DictConfig

class HTrack:
    def __init__(self, config: DictConfig):
        self.habits = {}
        self.config = self.check_config(config)
        self.save()

    def check_config(self, config):
        if not config.get('habits'):
            config.habits = {}
        else:
            for habit in config.habits:
                days = config.habits[habit]['days']
                self.habits[habit] = Habit(habit, days)
        return config

    def save(self):
        habits = {}
        for name in self.habits:
            habits[name] = self.habits[name].as_dict()
        self.config.habits = habits

        OmegaConf.save(self.config, tracker_path())

    def create_habit(self, name):
        if not self.config.get(name):
            habit = Habit(name)
            self.habits[name] = habit
        self.save()
    
    def list(self):
        for habit in self.habits:
            print(habit)

    def complete_habit(self, habit):
        self.habits[habit].complete()
        self.save() 

    def timeline(self, days=7):
        self.timeline = '{}'.format(' '*self._max_length_word(), end='')        
        self._add_date_line(days)
        self._add_habit_line()
        print(self.timeline)         

    def _add_date_line(self, days):        
        self.dates = []
        for day in range(days-1, -1,-1):
            that_day = datetime.datetime.now() - datetime.timedelta(days=day)
            pretty_date = str(that_day.month) + '/' + str(that_day.day)
            self.timeline += ' {:^7}'.format(pretty_date)
            self.dates.append(that_day)
        self.timeline += '\n'

    def _add_habit_line(self):
        for habit in self.habits:
            self.timeline += habit + ''*(self._max_length_word() - len(habit))
            for day in self.dates:
                if self.habits[habit].day_complete(day):
                    self.timeline += ' {:^7}'.format('X')
                else:
                    self.timeline += ' {:^7}'.format('')
            self.timeline += '\n'  

    def _max_length_word(self):
        return len(max(self.habits, key=len))


    def plot(self, days=7):
        """
        show graph of completed habits last week
        """
        dates = []
        pretty_dates = []
        for day in range(days-1, -1, -1):
            that_day = datetime.datetime.now() - datetime.timedelta(days=day)
            pretty_date = str(that_day.month) + '/' + str(that_day.day)
            pretty_dates.append(pretty_date)
            dates.append(that_day)
        completed = []
        for day in dates:
            total = 0
            for habit in self.habits:
                if self.habits[habit].day_complete(day):
                    total += 1
            completed.append(total)
        from matplotlib import pyplot as plt
        plt.style.use('ggplot')
        plt.bar(pretty_dates, completed, color='green')
        plt.xlabel('Days')
        plt.ylabel('Completed habits')
        plt.show()

class Habit:
    def __init__(self, name: str, days: dict={}):
        """
        name: name lol
        days: dict days completed
        """
        self.name = name
        self.days = days

    def as_dict(self):
        return {'days': self.days}
    
    def complete(self):
        """
        days are represented as timestamps in str
        """
        current_day = datetime.datetime.today()
        timestamp = str(int(current_day.timestamp()))
        if not self.day_complete(current_day):
            self.days[timestamp] = True
    

    def day_complete(self, day):
        for time_ in self.days:
            other_day = datetime.datetime.fromtimestamp(int(time_))
            if (
                day.day == other_day.day 
                and day.month == other_day.month 
                and day.year == other_day.year
            ):
                return True
        return False


def tracker_dir_path():
    home = os.environ['HOME']
    path = os.path.join(home, '.local', 'share', 'htrack')
    return path

def tracker_path():
    path = os.path.join(tracker_dir_path(), 'config.yaml')
    return path

def check_tracker():
    config_path = tracker_path()
    dir_path = tracker_dir_path()
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        OmegaConf.save(OmegaConf.create(), config_path)
        return config_path
    else: 
        return None

def get_tracker():
    config_path = tracker_path()
    config = OmegaConf.load(config_path)
    htrack = HTrack(config)
    return htrack

@click.group()
def cli():
	pass

@cli.command(name='setup')
def setup():
    check_tracker()

@cli.command(name='habits')
@click.option('-n', 'name')
@click.option('-c', 'habit')
@click.option('-l', is_flag=True)
def habits(name, l, habit):
    htrack = get_tracker()
    if name:
        htrack.create_habit(name)
    if l:
        htrack.list()
    if habit:
        htrack.complete_habit(habit)

@cli.command(name='plot')
@click.option('-d', 'days', default=7)
def graph(days):
    htrack = get_tracker()
    htrack.plot(int(days))
    

@cli.command(name='timeline')
@click.option('-d', 'days', default=7)
def timeline(days):
    htrack = get_tracker()
    htrack.timeline(int(days))
    
if __name__ == '__main__':
    cli()
