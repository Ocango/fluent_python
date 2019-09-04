import random
import collections
import queue
import argparse

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5#发车间隔

Event = collections.namedtuple('Event','time proc action')

def taxi_process(ident,trips,start_time = 0):
    """每次状态改变时创建事件，把控制权让给仿真器"""
    time = yield Event(start_time,ident,'leave garage')
    for i in range(trips):#每辆taxi接客数，这里按（id+1）*2算的
        time = yield Event(time,ident,'pick up passenger')
        time = yield Event(time,ident,'drop off passenger')
    
    yield Event(time,ident,'going home')
    #结束出租车的进程

class Simulator():
    def __init__(self,procs_map):
        self.events = queue.PriorityQueue()#优先级队列,最小值优先被消耗掉
        self.procs = dict(procs_map)
    
    def run(self,end_time):
        """调度并显示事件，直到时间结束"""
        #调度每一个出租车的第一个事件。进入第一个yield预备，并存下第一个状态
        for _,proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)
        
        #此次仿真的主循环
        sim_time = 0
        while sim_time<end_time:
            if self.events.empty():
                print('*** end of events ***')
                break
            
            current_event = self.events.get()
            sim_time,proc_id,previous_action = current_event
            print('taxi:',proc_id,proc_id*'  ',current_event)#输出当前taxi的当前状态
            active_proc = self.procs[proc_id]#取得当前taxi的生成器
            next_time = sim_time + compute_duration(previous_action)#准备生成器下一个状态，推入下一个状态
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:#生成器已退出，可以直接把taxi移除了
                del self.procs[proc_id]
            else:
                self.events.put(next_event)#taxi放回去，用完了
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))



def compute_duration(previous_action):
    """利用指数分布计算操作的耗时"""
    if previous_action in ['leave garage','drop off passenger']:
        #新状态是四处徘徊
        interval = SEARCH_DURATION

    elif previous_action == 'pick up passenger':
        #新状态行程开始
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('未知的状态：%s' % previous_action)
    return int(random.expovariate(1/interval))+1

def main(end_time=DEFAULT_END_TIME,num_taxis = DEFAULT_NUMBER_OF_TAXIS,seed = None):
    """初始化随机生成器，构建过程，运行仿真程序"""
    if seed is not None:
        random.seed(seed)#这就是种子，roguolike游戏中极为常见的随机种子
    taxis = {
        #开启每个taxi的生成器，并传入了初始值
        i:taxi_process(i,(i+1)*2,i*DEPARTURE_INTERVAL) for i in range(num_taxis)
    }
    sim = Simulator(taxis)
    sim.run(end_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Taxi fleet simulator.')
    parser.add_argument('-e','--end-time',type=int,default=DEFAULT_END_TIME,help='simulation end time; default = %s' % DEFAULT_END_TIME)
    parser.add_argument('-t','--taxis',type=int,default=DEFAULT_NUMBER_OF_TAXIS,help='numbers of taxis running; default = %s' % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s','--seed',type=int,default=None,help='random generator seed (for testing)')
    args = parser.parse_args()
    main(args.end_time,args.taxis,args.seed)