filenames = ["file1","file2","file3","file4"]
drawings  = ["001","002","003","004"]
revisions = ["aaa","bbb","ccc","ddd"]

big_dict = {}
# counter = 0


for filename,drawing,revision in zip(filenames,drawings,revisions):
    big_dict[filename] = [drawing,revision]
    # counter += 1

print((big_dict))