import os
import time
import torch
import numpy as np
import numpy.random as rd
from copy import deepcopy
from replay import ReplayBuffer, ReplayBufferMP


"""[ElegantRL](https://github.com/AI4Finance-LLC/ElegantRL)"""


class Arguments:
    def __init__(self, agent=None, env=None, gpu_id=None, if_on_policy=False):
        self.agent = agent  # Deep Reinforcement Learning algorithm
        self.cwd = None  # current work directory. cwd is None means set it automatically
        self.env = env  # the environment for training
        self.env_eval = None  # the environment for evaluating
        self.gpu_id = gpu_id  # choose the GPU for running. gpu_id is None means set it automatically
        self.bubushu = 0
        '''Arguments for training (off-policy)'''
        self.net_dim = 2 ** 8  # the network width
        self.batch_size = 2 ** 8  # num of transitions sampled from replay buffer.
        self.repeat_times = 2 ** 0  # repeatedly update network to keep critic's loss small
        self.target_step = 2 ** 10  # collect target_step, then update network
        self.max_memo = 2 ** 17  # capacity of replay buffer
        if if_on_policy:  # (on-policy)
            self.net_dim = 2 ** 9
            self.batch_size = 2 ** 9
            self.repeat_times = 2 ** 4
            self.target_step = 2 ** 12
            self.max_memo = self.target_step
        self.gamma = 0.99  # discount factor of future rewards
        self.reward_scale = 2 ** 0  # an approximate target reward usually be closed to 256
        self.if_per = False  # Prioritized Experience Replay for sparse reward

        self.rollout_num = 1  # the number of rollout workers (larger is not always faster)
        self.num_threads = 1  # cpu_num for evaluate model, torch.set_num_threads(self.num_threads)

        '''Arguments for evaluate'''
        self.break_step = 2 ** 20  # break training after 'total_step > break_step'
        self.if_remove = True  # remove the cwd folder? (True, False, None:ask me)
        self.if_allow_break = True  # allow break training when reach goal (early termination)
        self.eval_gap = 2 ** 5  # evaluate the agent per eval_gap seconds
        self.eval_times1 = 2 ** 2  # evaluation times
        self.eval_times2 = 2 ** 4  # evaluation times if 'eval_reward > max_reward'
        
                
        import sys
        import os
        import re
        
        
        curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
        parent_path = os.path.dirname(curr_path)  # 父路径
        sys.path.append(parent_path)  # 添加路径到系统路径
        
        name=os.path.basename(__file__)
        print(name)
        
        #去掉文件后缀，只要文件名称
        # name=os.path.basename(__file__).split(".")[0]
        # print(name)
        
        
        your_daddad= os.path.basename(curr_path)
        
        d = re.findall(r"s_(.+?)",your_daddad)
        #d = int(d[0]) 
        d = int(d[0]) 
        print('d',d)
        
        self.random_seed = 10**(d-1)  # initialize random seed in self.init_before_training()
        
        print('self.random_seed',self.random_seed)
        
        self.allstep_num = 0
        
        self.zongr = 0
        
        self.bubu = 0

    def init_before_training(self, if_main=True):
        if self.agent is None:
            raise RuntimeError('\n| Why agent=None? Assignment args.agent = AgentXXX please.')
        if not hasattr(self.agent, 'init'):
            raise RuntimeError('\n| There should be agent=AgentXXX() instead of agent=AgentXXX')
        if self.env is None:
            raise RuntimeError('\n| Why env=None? Assignment args.env = XxxEnv() please.')
        if isinstance(self.env, str) or not hasattr(self.env, 'env_name'):
            raise RuntimeError('\n| What is env.env_name? use env=PreprocessEnv(env). It is a Wrapper.')

        '''set gpu_id automatically'''
        if self.gpu_id is None:  # set gpu_id automatically
            import sys
            self.gpu_id = sys.argv[-1][-4]
        else:
            self.gpu_id = str(self.gpu_id)
        if not self.gpu_id.isdigit():  # set gpu_id as '0' in default
            self.gpu_id = '0'

        '''set cwd automatically'''
        # if self.cwd is None:
        #     agent_name = self.agent.__class__.__name__
            #self.cwd = f'./{agent_name}/{self.env.env_name}_{self.gpu_id}'
        agent_name = self.agent.__class__.__name__    
        self.cwd = f'./{agent_name}/{self.env.env_name}_{0}'

        if if_main:
            print(f'| GPU id: {self.gpu_id}, cwd: {self.cwd}')

            import shutil  # remove history according to bool(if_remove)
            if self.if_remove is None:
                self.if_remove = bool(input("PRESS 'y' to REMOVE: {}? ".format(self.cwd)) == 'y')
            if self.if_remove:
                shutil.rmtree(self.cwd, ignore_errors=True)
                print("| Remove history")
            os.makedirs(self.cwd, exist_ok=True)

        os.environ['CUDA_VISIBLE_DEVICES'] = str(self.gpu_id)
        torch.set_num_threads(self.num_threads)
        torch.set_default_dtype(torch.float32)
        torch.manual_seed(self.random_seed)
        np.random.seed(self.random_seed)


'''single process training'''




def train_and_evaluate(args,initial,end):
    
    chaochucishu_forshoulian_last = 0
    
    meicitupodebu_0=[]    
    meicitupodebu_1=[]
    meicitupodebu_2=[]
    # meicitupodebu_3=[]
    # meicitupodebu_4=[]
    # meicitupodebu_5=[]
    
    log_all = np.array([[0,0,0]])
    

 
    args.net_dim = int(2 ** 6)
    
    args.max_step = args.env.max_step
    #args.max_memo = (args.max_step - 1) * 8  # capacity of replay buffer
    args.target_step = args.allstep_num*(2**10)
    
    args.break_step = 10000000*args.target_step
    
    args.max_memo =  args.target_step
    
    args.gpu_id = '10'
    
    args.batch_size = int(args.max_memo/512)
    
    #args.repeat_times = 2**12 # int(2 **6) # repeatedly update network to keep critic's loss small
    
    
    
    
    zongr = 0
    zongbu = 0
    nayibu = 0
    dijicitupo = 0
    
    dijicitupo_jihe = []
    
    dianfengdian = []
    
    dianhouzhongdian = []
    
    args.init_before_training()
    
    # geshu =  [1000,1500,1500,2000,2000]
    
    # xuexirate = [1e-5,1e-6,1e-6,1e-7,1e-7]
    
    # ratio_clip_beiyong = [0.2,0.2,0.2,0.2,0.2]
    
    # lambda_entropy_beiyong = [0.04,0.04,0.02,0.02,0.01]
    
    
    # geshu =  [1000,1500,2000]
    
    # xuexirate = [1e-5,5e-6,1e-6]
    
    # ratio_clip_beiyong = [0.2,0.2,0.2]
    
    # lambda_entropy_beiyong = [0.02,0.01,0.005]
    
    geshu =  [200,200,200]
    
    xuexirate = [1e-4,1e-5,1e-6]
    
    ratio_clip_beiyong = [0.15,0.15,0.15]
    
    lambda_entropy_beiyong = [0.01,0.005,0.0025]   
    
    repeat_times_zu = [2**4,2**4,2**4]
     
    
    args.repeat_times = repeat_times_zu[0]
    
    
    xuanxiang = 0
    
    chaobiaozhishiwu = 0
    
    
    
    
    
    
    jici = 0
    '''basic arguments'''
    cwd = args.cwd
    env = args.env
    agent = args.agent
    gpu_id = args.gpu_id  # necessary for Evaluator?
    bubushu = args.bubushu 

    '''training arguments'''
    net_dim = args.net_dim
    max_memo = args.max_memo
    break_step = args.break_step
    batch_size = args.batch_size
    target_step = args.target_step
    repeat_times = args.repeat_times
    if_break_early = args.if_allow_break
    if_per = args.if_per
    gamma = args.gamma
    reward_scale = args.reward_scale
    
    bubu =  args.bubu
    

    '''evaluating arguments'''
    eval_gap = args.eval_gap
    eval_times1 = args.eval_times1
    eval_times2 = args.eval_times2
    if args.env_eval is not None:
        env_eval = args.env_eval
    elif args.env_eval in set(gym.envs.registry.env_specs.keys()):
        env_eval = PreprocessEnv(gym.make(env.env_name))
    else:
        env_eval = deepcopy(env)

    del args  # In order to show these hyper-parameters clearly, I put them above.

    '''init: environment'''
    max_step = env.max_step
    state_dim = env.state_dim
    action_dim = env.action_dim
    if_discrete = env.if_discrete

    '''init: Agent, ReplayBuffer, Evaluator'''
    agent.init(net_dim, state_dim, action_dim, if_per)
    if_on_policy = getattr(agent, 'if_on_policy', False)

    buffer = ReplayBuffer(max_len=max_memo, state_dim=state_dim, action_dim=1 if if_discrete else action_dim,
                          if_on_policy=if_on_policy, if_per=if_per, if_gpu=True)

    evaluator1 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
                          eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=1,initial=initial,end=end)
    # evaluator2 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=2)
    # evaluator3 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=3)
    # evaluator4 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=4)

    # evaluator5 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=5)
    # evaluator6 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=6)
    
    # evaluator7 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=7)
    # evaluator8 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=8)
    # evaluator9 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=9)
    
    # evaluator10 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=10)
    # evaluator11 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2,bubu=bubu, casenum=11)
    # evaluator12 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2, casenum=12)
    # evaluator13 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2, casenum=13)
    # evaluator14 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2, casenum=14)
    # evaluator15 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2, casenum=15)
    # evaluator16 = Evaluator(cwd=cwd, agent_id=gpu_id, device=agent.device, env=env_eval,
    #                       eval_gap=eval_gap, eval_times1=eval_times1, eval_times2=eval_times2, casenum=16) 
     
    with torch.no_grad():  # 收集
        fuckless = explore_before_training(env, buffer, max_memo , reward_scale, gamma)    
    
    path2 =os.path.abspath(os.path.join(os.getcwd(), "../../.."))
    '''prepare for training'''
    agent.state = env.reset()
    if if_on_policy:
        steps = 0
    else:  # explore_before_training for off-policy
        with torch.no_grad():  # update replay buffer
            steps = explore_before_training(env, buffer, target_step, reward_scale, gamma)

        agent.update_net(buffer, target_step, batch_size, repeat_times)  # pre-training and hard update
        agent.act_target.load_state_dict(agent.act.state_dict()) if getattr(agent, 'act_target', None) else None
        agent.cri_target.load_state_dict(agent.cri.state_dict()) if getattr(agent, 'cri_target', None) else None
    total_step = steps

    '''start training'''

    path_now = evaluator1.cwd
    
    initial_zifu = str(evaluator1.initial)
    
    end_zifu = str(evaluator1.end)      
        
    shenjing_dateguiyi =path2 + '\\'+ 'guiyi_' + initial_zifu + 'to' + end_zifu +'_case'+str(evaluator1.casenum)+'_'+ str(evaluator1.bubu)+'bu'+'.pth.npy'
    
    if os.path.exists(shenjing_dateguiyi):
            
        buffer.cunchu = np.load(shenjing_dateguiyi)
        
        buffer.guiyi_initial()




    path_now = evaluator1.cwd

    initial_zifu = str(evaluator1.initial)
    
    end_zifu = str( evaluator1.end )
    
    shenjing = path2 + '\\'+ 'actor_' + initial_zifu + 'to' + end_zifu +'_case1_0bu.pth'
    
    if os.path.exists(shenjing_dateguiyi):
    
        agent.act.load_state_dict(torch.load(shenjing))






    path_now = evaluator1.cwd

    initial_zifu = str(evaluator1.initial)
    
    end_zifu = str( evaluator1.end )
    
    shenjing = path2 + '\\'+'critic_' + initial_zifu + 'to' + end_zifu +'_case1_0bu.pth'
    
    shenjing_tar =path2 + '\\'+ 'critic_target_' + initial_zifu + 'to' + end_zifu +'_case1_0bu.pth'
    
    if os.path.exists(shenjing):
        
        agent.cri.load_state_dict(torch.load(shenjing))

        agent.cri_target.load_state_dict(torch.load(shenjing_tar))
        
        print('fuck new cri and cri_target')
    
    
    if_reach_goal = False
    while not ((if_break_early and if_reach_goal)
               or total_step > break_step
               or os.path.exists(f'{cwd}/stop')):


        
        print('————————————————————————————————————————————————————————————————————————————————————————————')
        if xuanxiang == 0:
            
            repeat_times = repeat_times_zu[xuanxiang]
            
            agent.learning_rate = xuexirate[xuanxiang]
            
            agent.optimizer = torch.optim.Adam([{'params': agent.act.parameters(), 'lr': agent.learning_rate},
                                               {'params': agent.cri.parameters(), 'lr': agent.learning_rate}])            
            agent.ratio_clip = ratio_clip_beiyong[xuanxiang]  # could be 0.2 ~ 0.5, ratio.clamp(1 - clip, 1 + clip),
            agent.lambda_entropy = lambda_entropy_beiyong[xuanxiang]

            
        if zongbu-nayibu == geshu[xuanxiang] :#and zongbu-nayibu >= chaochucishu_forshoulian_last*4 :
            
            dijicitupo_jihe.append(dijicitupo)
            
            dianfengdian.append(nayibu)
            
            dianhouzhongdian.append(zongbu)
            
            print('huanpeizhile')
            
            xuanxiang = xuanxiang + 1
            

            
            
            
            if xuanxiang > len(geshu)-1:
                
            #     xuanxiang = xuanxiang - 1
                
                chaobiaozhishiwu = 1
                
                #buffer.xuejiangeshu(geshu[xuanxiang-1]*40*(2**4))
                
               
                
                break
            
            nayibu = zongbu
                
            dijicitupo = 0


            path_now = evaluator1.cwd
            
            initial_zifu = str(evaluator1.initial)
            
            end_zifu = str(evaluator1.end)
            
            shenjing_act = 'actor_' + initial_zifu + 'to' + end_zifu +'_case'+str(evaluator1.casenum)+'_'+ str(evaluator1.bubu)+'bu'+'.pth'
            
            wangluo_act_path = path_now+ '\\'+shenjing_act
            
            agent.act.load_state_dict(torch.load(wangluo_act_path))
            
            print('fuck chongxin act')         
            
            
            

            shenjing_cri = 'critic_' + initial_zifu + 'to' + end_zifu +'_case'+str(evaluator1.casenum)+'_'+ str(evaluator1.bubu)+'bu'+'.pth'
            
            wangluo_cri_path = path_now+ '\\'+shenjing_cri            
            
            agent.cri.load_state_dict(torch.load(wangluo_cri_path))  

            print('fuck chongxin cri')            
            
            #buffer.xuejiangeshu(geshu[xuanxiang-1]*40*(2**4))
 



            shenjing_cri = 'critic_target_' + initial_zifu + 'to' + end_zifu +'_case'+str(evaluator1.casenum)+'_'+ str(evaluator1.bubu)+'bu'+'.pth'
            
            wangluo_cri_target_path = path_now+ '\\'+shenjing_cri            
            
            agent.cri_target.load_state_dict(torch.load(wangluo_cri_target_path)) 
            
            print('fuck chongxin cri_target')


  
                
            shenjing_dateguiyi = 'guiyi_' + initial_zifu + 'to' + end_zifu +'_case'+str(evaluator1.casenum)+'_'+ str(evaluator1.bubu)+'bu'+'.pth.npy'

            dataguiyi__path = path_now+ '\\'+shenjing_dateguiyi            
            
            buffer.cunchu = np.load(dataguiyi__path)
            
            buffer.guiyi_initial()
            
            print('fuck chongxin guiyi')
            
            repeat_times = repeat_times_zu[xuanxiang]

 
            
            agent.learning_rate = xuexirate[xuanxiang]
            
            agent.optimizer = torch.optim.Adam([{'params': agent.act.parameters(), 'lr': agent.learning_rate},
                                               {'params': agent.cri.parameters(), 'lr': agent.learning_rate}])            
            agent.ratio_clip = ratio_clip_beiyong[xuanxiang]  # could be 0.2 ~ 0.5, ratio.clamp(1 - clip, 1 + clip),
            agent.lambda_entropy = lambda_entropy_beiyong[xuanxiang]
            
            
            
            
        print('chaochushuliang:  ',zongbu-nayibu)
        
        
        

        with torch.no_grad(): 
        
            time_start = time.time()
            steps = agent.explore_env(env, buffer, target_step, reward_scale, gamma)
            time_end = time.time()
            time_c= time_end - time_start
            print('time cost', time_c, 's')
            
        total_step += steps


        zongbu=zongbu+1
        
        time_start = time.time()

        obj_a, obj_c = agent.update_net(buffer, target_step, batch_size, repeat_times)
        time_end = time.time()
        time_c= time_end - time_start
        print('tratime cost', time_c, 's')
        with torch.no_grad(): 
        
            if_reach_goal1,r1,neibudiedaidaolema,shangxiajiaocuo = evaluator1.evaluate_save(agent.act, agent.cri,agent.cri_target, steps, obj_a, obj_c,buffer)
            evaluator1.draw_plot()

        # if_reach_goal2,r2,_ = evaluator2.evaluate_save(agent.act, agent.cri, steps, obj_a, obj_c,buffer)
        # evaluator2.draw_plot()

        # if_reach_goal3,r3,_ = evaluator3.evaluate_save(agent.act, agent.cri, steps, obj_a, obj_c,buffer)
        # evaluator3.draw_plot()
        
        # if_reach_goal4,r4,_ = evaluator4.evaluate_save(agent.act, agent.cri, steps, obj_a, obj_c,buffer)
        # evaluator4.draw_plot()        
        
        # if_reach_goal5,r5,_ = evaluator5.evaluate_save(agent.act, agent.cri, steps, obj_a, obj_c,buffer)
        # evaluator5.draw_plot()  
 
        # if_reach_goal6,r6,_ = evaluator6.evaluate_save(agent.act, agent.cri, steps, obj_a, obj_c,buffer)
        # evaluator6.draw_plot()         

        # if_reach_goal7,r7,_ = evaluator7.evaluate_save(agent.act, agent.cri, steps, obj_a, obj_c,buffer)
        # evaluator7.draw_plot() 

        # if_reach_goal8,r8,_ = evaluator8.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        # evaluator8.draw_plot() 

        # if_reach_goal9,r9,_ = evaluator9.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        # evaluator9.draw_plot() 
        
        # if_reach_goal10,r10,_ = evaluator10.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        # evaluator10.draw_plot() 

        # if_reach_goal11,r11,neibudiedaidaolema = evaluator11.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        #evaluator1.draw_plot()
        
        # if_reach_goal12,r12 = evaluator12.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        # evaluator12.draw_plot()        
        
        # if_reach_goal13,r13 = evaluator13.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        # evaluator13.draw_plot()        
        
        # if_reach_goal4,r14 = evaluator14.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        # evaluator14.draw_plot()         

        # if_reach_goal5,r15 = evaluator15.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        # evaluator15.draw_plot() 

        # if_reach_goal6,r16 = evaluator16.evaluate_save(agent.act, steps, obj_a, obj_c,buffer)
        # evaluator16.draw_plot()         
 
        rping =    r1        # r1+r2+r3+r4     #+r5 + r6+r7+r8+r9+r10 +r11+r12+r13+r14+r15+r16)
        

        
        
        if zongr <= rping:
            
            
            zongr = rping
            
            chaochucishu_forshoulian_last = zongbu - nayibu
            
            nayibu = zongbu
            
            shangxiachaochu_nayibu = shangxiajiaocuo
            
            
            initial_zifu = str(evaluator1.initial)
            
            end_zifu = str(evaluator1.end)
            
            log_all = np.vstack((log_all,np.array([zongr,r1,nayibu])))
            
            np.save(initial_zifu+'to'+end_zifu+'pingjunzuida_zhi_he_bushu.npy',log_all)
            

            dijicitupo = dijicitupo + 1
        
            evaluator1.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)
            
            
            
    
    
            if xuanxiang==0:
                
                meicitupodebu_0.append(nayibu)
                
            if xuanxiang==1:
                
                meicitupodebu_1.append(nayibu)     
                
            if xuanxiang==2:
                
                meicitupodebu_2.append(nayibu) 
            
            # if xuanxiang==3:
                
            #     meicitupodebu_3.append(nayibu)
                
            # if xuanxiang==4:
                
            #     meicitupodebu_4.append(nayibu)     
                
            # if xuanxiang==5:
                
            #     meicitupodebu_5.append(nayibu)
    

            # evaluator2.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)
    
            # evaluator3.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)
            
            # evaluator4.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)

            # evaluator5.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)
            
            # evaluator6.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)

            # evaluator7.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)
            
            # evaluator8.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)

            # evaluator9.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)
            
            # evaluator10.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)
            
            # evaluator11.chuhaotu(agent.act, steps, obj_a, obj_c,buffer)

        
        print('zongbu',zongbu)
        
        print('dangqianjiang',rping)
        
        print('dangqianshangxiajiaocuo',shangxiajiaocuo)
        
        print('pingjunzuida',zongr)
        
        #print('pingjunzuidadebu',nayibu)
        
        #print('pingjunzuidashangxiajiaocuo',shangxiachaochu_nayibu)
                
        
        print('r1  ',r1)
        # print('r2  ',r2)
        # print('r3  ',r3)
        # print('r4  ',r4)
        # print('r5  ',r5)
        # print('r6  ',r6)    
        # print('r7  ',r7)
        # print('r8  ',r8)
        # print('r9  ',r9)
        # print('r10  ',r10)  
        # print('r11  ',r11) 
        
        
        
        print('xuanxiang',xuanxiang)
        
        if chaobiaozhishiwu == 1:
            
            print('chaobiao')
            
        # if neibudiedaidaolema==True and zongbu>3000:
        #     break        
        
        print('dianfengdian',dianfengdian)
        
        print('dijicitupo',dijicitupo)
        
        print('dianfengdianzhongdian',dianhouzhongdian)
        
        print('dijicitupo_jihe',dijicitupo_jihe)
        
        print('meicitupodebu_0',meicitupodebu_0)
        
        print('meicitupodebu_1',meicitupodebu_1)
        
        print('meicitupodebu_2',meicitupodebu_2)
        
        # print('meicitupodebu_3',meicitupodebu_3)
        
        # print('meicitupodebu_4',meicitupodebu_4)
        
        print('chaochucishu_forshoulian_last',chaochucishu_forshoulian_last)
        
        #print('--------------------------------------------------------------------')

        
    #print(f'| SavedDir: {cwd}\n| UsedTime: {time.time() - evaluator.start_time:.0f}')



'''utils'''


class Evaluator:
    def __init__(self, cwd, agent_id, eval_times1, eval_times2, eval_gap, env, device, casenum,bubu,initial,end):
        self.recorder = [(0., -np.inf, 0., 0., 0.), ]  # total_step, r_avg, r_std, obj_a, obj_c
        self.r_max = -np.inf
        self.total_step = 0

        self.cwd = cwd  # constant
        self.device = device
        self.agent_id = agent_id
        self.eval_gap = eval_gap
        self.eval_times1 = eval_times1
        self.eval_times2 = eval_times2
        self.env = env
        self.target_return = env.target_return
        
        self.casenum = casenum

        self.used_time = None
        self.start_time = time.time()
        self.eval_time = -1  # a early time
        
        self.bubu = bubu
        
        self.initial = initial
        
        self.end = end
        
        self.neibushu  = 0
        print(f"{'ID':>2}  {'Step':>8}  {'MaxR':>8} |"
              f"{'avgR':>8}  {'stdR':>8}   {'objA':>8}  {'objC':>8} |"
              f"{'avgS':>6}  {'stdS':>4}")

    def evaluate_save(self, act,cri,cri_target, steps, obj_a, obj_c,buffer) -> bool:
        self.total_step += steps  # update total training steps

        if 1:
            self.eval_time = time.time()

            rewards_steps_list = [get_episode_return(self.env, act, self.device,buffer,self.casenum ) for _ in range(self.eval_times1)]
            
            #print('rewards_steps_list',rewards_steps_list)
            
            r_avg, r_std, s_avg, s_std,shangxiajiaocuo = self.get_r_avg_std_s_avg_std(rewards_steps_list)
            
            self.recorder.append((self.total_step, r_avg, r_std, obj_a, obj_c))  # update recorder
                
            self.neibushu  = self.neibushu  + 1
            # if r_avg > self.r_max:  # evaluate actor twice to save CPU Usage and keep precision
            #     rewards_steps_list += [get_episode_return(self.env, act, self.device)
            #                            for _ in range(self.eval_times2 - self.eval_times1)]
            #     r_avg, r_std, s_avg, s_std = self.get_r_avg_std_s_avg_std(rewards_steps_list)
            if r_avg >= self.r_max:  # save checkpoint with highest episode return
                self.r_max = r_avg  # update max reward (episode return)

                '''save actor.pth'''
                
                path_now = self.cwd
                
      
                initial_zifu = str(self.initial)
                
                end_zifu = str( self.end )
                
                shenjing = 'actor_' + initial_zifu + 'to' + end_zifu +'_case'+str(self.casenum)+'_'+ str(self.bubu)+'bu'+'.pth'
                
                path_actor = path_now+ '\\'+shenjing
                
                #act_save_path = f'{self.cwd}/actor.pth'
                torch.save(act.state_dict(), path_actor)
                

                '''save cri.pth'''
                
                path_now = self.cwd
                
      
                initial_zifu = str(self.initial)
                
                end_zifu = str( self.end )
                
                shenjing = 'critic_' + initial_zifu + 'to' + end_zifu +'_case'+str(self.casenum)+'_'+ str(self.bubu)+'bu'+'.pth'
                
                path_critic = path_now+ '\\'+shenjing
                
                #act_save_path = f'{self.cwd}/actor.pth'
                torch.save(cri.state_dict(), path_critic)                
                
                
                
                
                path_now = self.cwd
                
      
                initial_zifu = str(self.initial)
                
                end_zifu = str( self.end )
                
                shenjing = 'critic_target_' + initial_zifu + 'to' + end_zifu +'_case'+str(self.casenum)+'_'+ str(self.bubu)+'bu'+'.pth'
                
                path_critic_tar = path_now+ '\\'+shenjing
                
                #act_save_path = f'{self.cwd}/actor.pth'
                torch.save(cri_target.state_dict(), path_critic_tar)                   
                
                
                
                
                
                
                
                
                path_now = self.cwd
                
                initial_zifu = str(self.initial)
                
                end_zifu = str(self.end)      
                
                shenjing_dateguiyi = 'guiyi_' + initial_zifu + 'to' + end_zifu +'_case'+str(self.casenum)+'_'+ str(self.bubu)+'bu'+'.pth'
                
                dateguiyi_path = path_now+ '\\'+shenjing_dateguiyi
                
                np.save(dateguiyi_path,buffer.cunchu) 
                            
                
                print(f"{self.agent_id:<2}  {self.total_step:8.2e}  {self.r_max:8.2f} |")  # save policy and print
                #self.env.render(self.casenum)
                
                self.draw_plot(quan = False)
                
                self.neibushu = 0
                
                
                


            if_reach_goal = bool(self.r_max > self.target_return)  # check if_reach_goal
            if if_reach_goal and self.used_time is None:
                self.used_time = int(time.time() - self.start_time)
                print(f"{'ID':>2}  {'Step':>8}  {'TargetR':>8} |"
                      f"{'avgR':>8}  {'stdR':>8}   {'UsedTime':>8}  ########\n"
                      f"{self.agent_id:<2}  {self.total_step:8.2e}  {self.target_return:8.2f} |"
                      f"{r_avg:8.2f}  {r_std:8.2f}   {self.used_time:>8}  ########")

            print(f"{self.casenum:<2}  {self.total_step:8.2e}  {self.r_max:8.2f} |"
                  f"{r_avg:8.2f}  {r_std:8.2f}   {obj_a:8.2f}  {obj_c:8.2f} |"
                  f"{s_avg:6.0f}  {s_std:4.0f}")
            
            print('----------------------------------------------')
        else:
            if_reach_goal = False
            
        neibudiedaidaolema = False
        if self.neibushu > 2000:
            neibudiedaidaolema = True
            
        return if_reach_goal,r_avg,neibudiedaidaolema,shangxiajiaocuo

    def draw_plot(self, quan = True):
        if len(self.recorder) == 0:
            print("| save_npy_draw_plot() WARNNING: len(self.recorder)==0")
            return None
        
        
        pathh = self.cwd

        # initial = getattr(self.env, 'initial')
        # end = getattr(self.env, 'end')


        initial_zifu = str(self.initial)
        
        end_zifu = str( self.end )


        if quan:
            
            recorderwenjianjia = 'quanrecorder' + initial_zifu + 'to' + end_zifu +'_bu'+ str(self.bubu) +'_case' + str(self.casenum)
            
            if not os.path.exists(pathh+'\\' + recorderwenjianjia):
                    
                os.mkdir(pathh+'\\' + recorderwenjianjia )
                
            yaowd = pathh+'\\' + recorderwenjianjia
            
 
        #data_save = os.path.join(pathh, '\\', wenjianjia, '\\', str(fucknum)+'.npy')
            data_save =pathh+ '\\'+ recorderwenjianjia+ '\\'+ 'quan_recorder.npy'
         
            np.save(data_save , self.recorder)
    
            '''draw plot and save as png'''
            train_time = int(time.time() - self.start_time)
            total_step = int(self.recorder[-1][0])
            save_title = f"plot_step_time_maxR_{int(total_step)}_{int(train_time)}_{self.r_max:.3f}"
    
            save_learning_curve(self.recorder, yaowd, save_title)
            
        else:
            
            recorderwenjianjia = 'recorder' + initial_zifu + 'to' + end_zifu +'_bu'+ str(self.bubu) + '_case' + str(self.casenum)
            
            if not os.path.exists(pathh+'\\' + recorderwenjianjia):
                    
                os.mkdir(pathh+'\\' + recorderwenjianjia )
                
            yaowd = pathh+'\\' + recorderwenjianjia
                
            #data_save = os.path.join(pathh, '\\', wenjianjia, '\\', str(fucknum)+'.npy')
            data_save =pathh+ '\\'+ recorderwenjianjia+ '\\'+ 'quan_recorder.npy'
             
            np.save(data_save , self.recorder)
        
            '''draw plot and save as png'''
            train_time = int(time.time() - self.start_time)
            total_step = int(self.recorder[-1][0])
            save_title = f"plot_step_time_maxR_{int(total_step)}_{int(train_time)}_{self.r_max:.3f}"
        
            save_learning_curve(self.recorder, yaowd, save_title)            
            
        
        
        
        

    @staticmethod
    def get_r_avg_std_s_avg_std(rewards_steps_list):
        rewards_steps_ary = np.array(rewards_steps_list)
        r_avg, s_avg,jiaocuo_avg = rewards_steps_ary.mean(axis=0)  # average of episode return and episode step
        r_std, s_std,_ = rewards_steps_ary.std(axis=0)  # standard dev. of episode return and episode step
        return r_avg, r_std, s_avg, s_std,jiaocuo_avg



    def chuhaotu(self, act, steps, obj_a, obj_c,buffer) -> bool:
        
        get_episode_return_chuhaotu(self.env, act, self.device,buffer,self.casenum )




def get_episode_return(env, act, device,buffer,casenum) -> (float, int):
    episode_return = 0.0  # sum of rewards in an episode
    episode_step = 1
    max_step = env.max_step
    if_discrete = env.if_discrete

    state = env.reset(casenum)
    for episode_step in range(max_step):
        
        state_out = buffer.guiyi.transform(state.reshape(1,-1))
        
        s_tensor = torch.as_tensor((state_out[0],), device=device)
        a_tensor = act(s_tensor)
        if if_discrete:
            a_tensor = a_tensor.argmax(dim=1)
        action = a_tensor.detach().cpu().numpy()[0]  # not need detach(), because with torch.no_grad() outside
        state, reward, done, _ = env.step(action)
        episode_return += reward
        if done:
            break
    
    env.quanrender(casenum)
    
    shangxiajiaocuo=0 #= env.jisuanshangxia()
    
    episode_return = getattr(env, 'episode_return', episode_return)
    return episode_return, episode_step + 1,shangxiajiaocuo


def save_learning_curve(recorder, cwd='.', save_title='learning curve'):
    recorder = np.array(recorder)  # recorder_ary.append((self.total_step, r_avg, r_std, obj_a, obj_c))
    steps = recorder[:, 0]  # x-axis is training steps
    r_avg = recorder[:, 1]
    r_std = recorder[:, 2]
    obj_a = recorder[:, 3]
    obj_c = recorder[:, 4]

    '''plot subplots'''
    import matplotlib as mpl
    mpl.use('Agg')
    """Generating matplotlib graphs without a running X server [duplicate]
    write `mpl.use('Agg')` before `import matplotlib.pyplot as plt`
    https://stackoverflow.com/a/4935945/9293137
    """
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2)

    axs0 = axs[0]
    axs0.cla()
    color0 = 'lightcoral'
    axs0.set_xlabel('Total Steps')
    axs0.set_ylabel('Episode Return')
    axs0.plot(steps, r_avg, label='Episode Return', color=color0)
    axs0.fill_between(steps, r_avg - r_std, r_avg + r_std, facecolor=color0, alpha=0.3)

    ax11 = axs[1]
    ax11.cla()
    color11 = 'royalblue'
    axs0.set_xlabel('Total Steps')
    ax11.set_ylabel('objA', color=color11)
    ax11.plot(steps, obj_a, label='objA', color=color11)
    ax11.tick_params(axis='y', labelcolor=color11)

    ax12 = axs[1].twinx()
    color12 = 'darkcyan'
    ax12.set_ylabel('objC', color=color12)
    ax12.fill_between(steps, obj_c, facecolor=color12, alpha=0.2, )
    ax12.tick_params(axis='y', labelcolor=color12)

    '''plot save'''
    plt.title(save_title, y=2.3)
    plt.savefig(f"{cwd}/plot_learning_curve.jpg")
    plt.close('all')  # avoiding warning about too many open figures, rcParam `figure.max_open_warning`
    # plt.show()  # if use `mpl.use('Agg')` to draw figures without GUI, then plt can't plt.show()


def explore_before_training(env, buffer, target_step, reward_scale, gamma) -> int:
    # just for off-policy. Because on-policy don't explore before training.
    if_discrete = env.if_discrete
    action_dim = env.action_dim

    state = env.reset()
    steps = 0
    
    shu = np.empty([target_step,env.state_dim])

    while steps < target_step:
        action = rd.randint(action_dim) if if_discrete else rd.uniform(-1, 1, size=action_dim)
        next_state, reward, done, _ = env.step(action)
        steps += 1

        scaled_reward = reward * reward_scale
        mask = 0.0 if done else gamma
        #other = (scaled_reward, mask, action) if if_discrete else (scaled_reward, mask, *action)
        # buffer.append_buffer(state, (0,0,0,0,0,0))
        shu=np.vstack((shu,next_state))

        state = env.reset() if done else next_state
        
    buffer.cunchu = shu
    
    buffer.guiyi_initial()
    
    return steps

def get_episode_return_chuhaotu(env, act, device,buffer,casenum) -> (float, int):
    episode_return = 0.0  # sum of rewards in an episode
    episode_step = 1
    max_step = env.max_step
    if_discrete = env.if_discrete

    state = env.reset(casenum)
    for episode_step in range(max_step):
        
        state_out = buffer.guiyi.transform(state.reshape(1,-1))
        
        s_tensor = torch.as_tensor((state_out[0],), device=device)
        a_tensor = act(s_tensor)
        if if_discrete:
            a_tensor = a_tensor.argmax(dim=1)
        action = a_tensor.detach().cpu().numpy()[0]  # not need detach(), because with torch.no_grad() outside
        state, reward, done, _ = env.step(action)
        episode_return += reward
        if done:
            break
    
    env.render(casenum)
