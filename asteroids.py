import json


def get_score(curr_score):
    if curr_score >= 10:
        return curr_score * 2
    elif curr_score > 7:
        return curr_score * 1.5
    else:
        return curr_score


def calc_asteroids(data_file):
    inp = json.loads(data_file)

    res_json = []
    for i, v in enumerate(inp["test_cases"]):
        res_json.append({"input": v, "score": 0, "origin": 0})

    res = []
    for string in inp["test_cases"]:
        if len(string) > 20:
            res.append((0, 0))
            continue
        maxx = -1
        index = -1
        for i in range(len(string)):
            total = 0
            curr_char = string[i]
            curr_score = 1

            left_ptr = i - 1
            right_ptr = i + 1
            while left_ptr >= 0 and string[left_ptr] == curr_char:
                left_ptr -= 1
                curr_score += 1
            while right_ptr < len(string) and string[right_ptr] == curr_char:
                right_ptr += 1
                curr_score += 1

            total += get_score(curr_score)

            while left_ptr > 0 or right_ptr < len(string) - 1:
                left_ptr -= 1
                right_ptr += 1
                
                left_score = 0
                right_score = 0

                left_char = -1
                right_char = 1

                if left_ptr >= 0:
                    left_char = string[left_ptr]
                    left_score = 1
                    while left_ptr >= 0 and string[left_ptr] == left_char:
                        left_ptr -= 1
                        left_score += 1
                
                if right_ptr < len(string):
                    right_char = string[right_ptr]
                    right_score = 1
                    while right_ptr < len(string) and string[right_ptr] == right_char:
                        right_ptr += 1
                        right_score += 1

                if left_char == right_char:
                    total += get_score(left_score + right_score)
                else:
                    total += get_score(left_score) + get_score(right_score)
            if total > maxx:
                maxx = total
                index = i
        res.append((maxx, index))
    res_json = []
    for i, v in enumerate(res):
        res_json.append({"input": inp["test_cases"][i], "score": v[0], "origin": v[1]})
    return res_json
