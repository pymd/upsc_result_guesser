import sys
filename = sys.argv[1]

try:
    f = open(filename,'r')
    lines = f.read()

    prev = 699999

    lines = lines.split('\n')
    #print type(lines)
    for line in lines:
        if line == '':
            print ''
            continue
        try:
            line_parts = line.split(":")
            next_str = line_parts[1]
            #print "prev=",prev,"next=",next_str
            nextint = int(next_str)
            if nextint - prev != 1:
                print "Found: prev=",prev,"next=",nextint
            prev = nextint
        except Exception as e:
            #print e
            print line

finally:
    f.close()
