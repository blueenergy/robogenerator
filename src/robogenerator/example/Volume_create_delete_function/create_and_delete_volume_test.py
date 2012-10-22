documentation ='''The case is to create and delete all kinds of volumes'''
suite_setup ='Connect to System'
suite_teardown='Disconnect from System'

force_tags ='''owner-***  team-*  phase-RT  '''


parameters_template = {'type': [ "Primary", "Logical", "Single", "Span", "Stripe", "Mirror", "RAID-5"]
             , 'size':[ "10", "100", "500", "1000", "5000", "10000", "40000"]
             , 'format_method':[ "quick","slow"]
             ,'file_system':['FAT', 'FAT32', 'NTFS']
             ,'cluster_size':['512', '1024', '2048', '4096', '8192', '16384', '32768', '65536']
             ,'compression':['on', 'off']         
             }

parameters = parameters_template
output_filename ='create_and_delete_all_kinds_of_volumes.html'

case_name_template = 'create and delete volume with different parameters'
case_step_template = '''create_and_delete_volume_test  ${type}  ${size}  ${format_method}  ${file_system}  ${cluster_size}  ${compression}'''


'''

#
# File systems have constraints on volume size
#
IF [FSYSTEM] = "FAT"   THEN [SIZE] <= 4096;
IF [FSYSTEM] = "FAT32" THEN [SIZE] <= 32000;

IF [FSYSTEM] in {"FAT", "FAT32"} or
  ([FSYSTEM] = "NTFS" and [CLUSTER] >4096)
THEN [COMPRESSION] = "off";
'''
def is_valid_combination(row):

    
    n=len(row)
    if n>=len(parameters):

        '''
            #
            # File systems have constraints on volume size
            #
            IF [FSYSTEM] = "FAT"   THEN [SIZE] <= 4096;
            IF [FSYSTEM] = "FAT32" THEN [SIZE] <= 32000;
        '''
        if row['file_system'] =="FAT" and row['size']>4096:
            return False
        if row['file_system'] =="FAT32" and row['size']>32000:
            return False
        '''
        # Compression can be applied only for volumes
        # formatted as NTFS and with cluster size <= 4K
        '''
        if row['file_system']  in ["FAT", "FAT32"] or (row['file_system'] == "NTFS" and row['cluster_size'] >4096):
            if row['compression'] =='ON':
                return False
            else:
                return True
        
    return True





if __name__=='__main__':

    pass




        
        
  




        
