#!/usr/bin/env python
"""
    18/11/2023
    Please don't mark this. This is task 1, but a joke.
"""
while True: numbers = list(filter(lambda a: a != None, [int(number) if number.isnumeric() else None for number in input("Enter whole numbers seperated by spaces below, e.g. (4 1 10 292 0)\n: ").split(" ")])) ; print(f"You inputted {len(numbers)} whole numbers\nStatistics of the given whole numbers:\nSum: {(lambda f: lambda *args: f(f, *args))(lambda self, f, seq, d: d if not seq else f(seq[0], self(self, f, seq[1:], d)))(lambda a,b: a+b, numbers, 0)}\nMean: {(lambda f: lambda *args: f(f, *args))(lambda self, f, seq, d: d if not seq else f(seq[0], self(self, f, seq[1:], d)))(lambda a,b: a+b, numbers, 0)/len(numbers):.2f}\nMin: {sorted(numbers)[0]}\nMax: {sorted(numbers)[-1]}\nPrimes: [{", ".join([str(number) for number in sorted(list(filter(lambda number: not (True in [number % i == 0 for i in range(2, number//2+1)]), numbers)))])}]") if len(numbers) else print("Try again")