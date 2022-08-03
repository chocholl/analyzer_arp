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


a0_df = pd.read_csv(params['a0'], sep=';')
if('exp' in a0_df.columns):
   a0_df.drop(['exp'], axis='columns', inplace=True)

a1_df = pd.read_csv(params['a1'], sep=';')
if('exp' in a1_df.columns):
   a1_df.drop(['exp'], axis='columns', inplace=True)

b_df = pd.read_csv(params['b'], sep=';')
if('exp' in b_df.columns):
   b_df.drop(['exp'], axis='columns', inplace=True)




#######################


arp_left = a0_df.merge(a1_df, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
arp_left.to_csv('_arp_left.csv', header=True, sep=';')


arp_left_to_b = arp_left.merge(b_df, how='left' ,on=['ip', 'mac'] )
arp_left_to_b.to_csv('_arp_left_to_b.csv',  sep=';')









