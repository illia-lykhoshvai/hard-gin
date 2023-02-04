import random
import math

args = {
    "num": int(),
    "lines": int(),
    "random-limits": float(),
    "functions": list(),
    "output_file": str()
}

math_f = {
    "exp": math.exp,
    "sin": math.sin,
    "cos": math.cos,
    "log2": math.log2,
    "log10": math.log10,
    "log_e": math.log
}

if __name__ == '__main__':
        
    args["num"] = int(input("Enter a number of arguments: "))
    args["lines"] = int(input("Enter a number of argument lines: "))
    args["random-limits"] = float(input("Enter a max. random factor (use . as separator): "))

    args["functions"] = list()
    header = "index"
    for index in range(args["num"]):
        while True:
            keys = math_f.keys()
            for name in keys:
                print(f"{name}")
            func_str = input("Enter function: ")
            try:
                func = math_f[func_str]
                args["functions"].append(func)
                func_name = input("Enter function name: ")
                header += "," + func_name
                break
            except:
                print("ha-ha, not funny")
                print("wrong function")

    args["output_file"] = input("Enter an output file name: ") + ".csv"
    line = [0 for _ in range(args["num"]+1)]
    try:
        f = open(args["output_file"],"x")
    except Exception as e:
        print("File with such name exists!")
        exit(2)

    f.write("sep=,\n")
    f.write(header+"\n")

    for line_iter in range(args["lines"]):
        line[0] = line_iter
        for x in range(1,args["num"]+1):
            func = args["functions"][x-1]
            try:
                line[x] = func(line_iter/5) + random.uniform(-1*args["random-limits"],args["random-limits"])
            except ValueError:
                line[x] = 0
        str_line = str(line)
        f.write(str_line.translate({ord(i): None for i in '[] '})+'\n')
    f.close()