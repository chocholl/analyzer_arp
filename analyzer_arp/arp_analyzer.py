import sys
import pandas as pd
import ast
import copy

def load_mapping(c_file_src_name):
    map_dict = {}
    with open(c_file_src_name, "r") as f:
        for line in f:
            #(key, val) = line.split(' ')
            spl = line.split(' ')
            #map_dict[spl[0]] = spl[1].rstrip()
            map_dict[spl[0].lower()] = spl[1].rstrip().lower()
    return map_dict


def print_result(p_f_name, p_keys_list, p_dict_list, is_screen=False):

   all_keys = []
   for t_s in p_dict_list:
      keys = t_s.keys()
      for k in keys:
         if ((k not in all_keys) and (k not in p_keys_list)):
            all_keys.append(k)
   if(len(all_keys)>0):
      all_keys.sort()

   f= open(p_f_name,"w")
   out=''
   p = p_keys_list + all_keys

   for pp in p:
      out = out + pp + ';'
   out = out[:-1]
   if (is_screen==True):
      print(out)
   f.write(out+"\n")

   for ss in p_dict_list:
      out = ''
      for pp in p:
         out = out + str(ss.get(pp, '')) + ';'
      out = out[:-1]
      if (is_screen==True):
         print(out)
      f.write(out+"\n")

   f.close() 



def get_result(p_f_name, is_screen=False):
   ret = []
   keys = []
   
   f = open(p_f_name)
   i = 0
   for line in f:
      l_line = line.rstrip()
      if(i==0):
         keys = l_line.split(';')
         i=i+1
      else:
         j=0
         d = {}
         for val in l_line.split(';'):
            if(val!=''):
               d[keys[j]]=val
            j=j+1
         ret.append(d)
   f.close()

   if( is_screen == True ):
      print(ret)

   return ret



params = load_mapping('params.txt')
a_list = []
b_list = []


a_list = ast.literal_eval(params['a_list'])
b_list = ast.literal_eval(params['b_list'])


mac1_list = []
mac2_list = []

if(False):
   for s in a_list:      
      c_mac = get_result(s)   
      for m1 in c_mac:
         found = False
         for m2 in mac1_list:         
            if(m1['mac'] == m2['mac'] and m1['vrf'] == m2['vrf'] and m1['ip'] == m2['ip']):
               found = True
               break
         if(found == False):
            m1_copy = copy.deepcopy(m1)
            mac1_list.append(m1_copy)

   for s in b_list:
      c_mac = get_result(s)   
      for m1 in c_mac:
         found = False
         for m2 in mac2_list:         
            if(m1['mac'] == m2['mac'] and m1['vrf'] == m2['vrf'] and m1['ip'] == m2['ip']):
               found = True
               break
         if(found == False):
            m1_copy = copy.deepcopy(m1)
            mac2_list.append(m1_copy)

   print_result("_arp1.csv", [], mac1_list)
   print_result("_arp2.csv", [], mac2_list)


df1 = pd.read_csv(a_list[0], sep=';')
if('exp' in df1.columns):
   df1.drop(['exp'], axis='columns', inplace=True)

df2 = pd.read_csv(b_list[0], sep=';')
if('exp' in df2.columns):
   df2.drop(['exp'], axis='columns', inplace=True)





#######################

arp_count_1 = df1.groupby('int')['ip'].count()
arp_count_2 = df2.groupby('int')['ip'].count()
arp_count_per_int = pd.DataFrame(arp_count_1).merge(pd.DataFrame(arp_count_2), how='outer', on='int' )
arp_count_per_int.to_csv('_arp_count_per_int.csv',  sep=';', header=['arp_count_1', 'arp_count_2'])

arp_count_1 = df1.groupby('vrf')['ip'].count()
arp_count_2 = df2.groupby('vrf')['ip'].count()
arp_count_per_vrf = pd.DataFrame(arp_count_1).merge(pd.DataFrame(arp_count_2), how='outer', on='vrf' )
arp_count_per_vrf.to_csv('_arp_count_per_vrf.csv',  sep=';', header=['arp_count_1', 'arp_count_2'])


arp_diff = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']!='both']
arp_diff.to_csv('_arp_diff.csv', header=True, sep=';')

arp_stable = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='both']
arp_stable.to_csv('_arp_stable.csv', header=True, sep=';')



arp_diff_per_vrf =  pd.DataFrame(arp_diff.groupby('vrf')['ip'].nunique())
arp_diff_per_vrf_vs_arp_count_per_vrf = pd.merge(arp_diff_per_vrf, arp_count_per_vrf, on='vrf')
arp_diff_per_vrf_vs_arp_count_per_vrf.to_csv('_arp_diff_per_vrf_vs_arp_count_per_vrf.csv', header=['arp_changed', 'arp_count_1', 'arp_count_2'], sep=';')


arp_diff_per_int =  pd.DataFrame(arp_diff.groupby('int')['ip'].nunique())
arp_diff_per_int_vs_arp_count_per_int = pd.merge(arp_diff_per_int, arp_count_per_int, on='int')
arp_diff_per_int_vs_arp_count_per_int.to_csv('_arp_diff_per_int_vs_arp_count_per_int.csv', header=['arp_changed', 'arp_count_1', 'arp_count_2'], sep=';')



df1 = pd.read_csv(a_list[0], sep=';')
df2 = pd.read_csv(b_list[0], sep=';')

if('exp' in df1.columns and 'exp' in df2.columns):
   
   mean_1 = df1.groupby('int')['exp'].mean().round(0)
   mean_2 = df2.groupby('int')['exp'].mean().round(0)
   exp_per_int = pd.DataFrame(mean_1).merge(pd.DataFrame(mean_2), how='outer', on='int' )
   exp_per_int.to_csv('_exp_mode_per_int.csv',  sep=';', header=['exp_1', 'exp_2'])

   exp_per_int_vs_arp_count = pd.merge(exp_per_int, arp_count_per_int, on='int')
   exp_per_int_vs_arp_count.to_csv('_exp_mode_per_int_vs_arp_count.csv',  sep=';')



   mean_1 = df1.groupby('vrf')['exp'].mean().round(0)
   mean_2 = df2.groupby('vrf')['exp'].mean().round(0)
   exp_per_vrf = pd.DataFrame(mean_1).merge(pd.DataFrame(mean_2), how='outer', on='vrf' )
   exp_per_vrf.to_csv('_exp_mode_per_vrf.csv',  sep=';', header=['exp_1', 'exp_2'])

   exp_per_vrf_vs_arp_count = pd.merge(exp_per_vrf, arp_count_per_vrf, on='vrf')
   exp_per_vrf_vs_arp_count.to_csv('_exp_mode_per_vrf_vs_arp_count.csv',  sep=';')

