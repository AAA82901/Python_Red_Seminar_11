def get_n_from_user(
        inp_msg: str,
        first_n: int,
        last_n: int,
        input_mistake_msg: str
) -> int:
    inp = input(inp_msg)
    while not inp.isdigit() or (inp := int(inp)) < first_n or last_n < inp:
        print(input_mistake_msg)
        inp = input(inp_msg)
    return inp
