
arr = ['https://848mitchell.com/floorplan/s1/',
        'https://848mitchell.com/floorplan/s2/',
        'https://848mitchell.com/floorplan/s3/']


def clean_slash(s):
    if s[-1] == '/':
        return s[:len(s)-1]


clean_arr = list(map(lambda x: clean_slash(x), arr))
# print(clean_arr)
res = list(map(lambda x: x.split('/')[-1], clean_arr))

print(res)