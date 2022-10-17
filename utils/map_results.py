names = {
    0: "Hamburger",
    1.0: "Pancake",
    2.0: "French_fries",
    3.0: "Broccoli",
    4.0: "Banana",
    5.0: "Pizza",
}


def classes(in_result: float) -> str:
    # out_results = list(map(names.get, in_results))
    out_results = names[in_result]
    return out_results


if __name__ == "__main__":
    classes
