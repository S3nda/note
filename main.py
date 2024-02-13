import yaml
import fire
import datetime
import random
from colorama import Fore
import time


def similarity(t1, t2):
    t1 = set(t1.split())
    t2 = set(t2.split())
    intersection = len(t1.intersection(t2))
    union = len(t1.union(t2))
    return intersection / union


def save(dictionnary):
    with open("content.yml", "w") as file:
        yaml.dump(dictionnary, file)


def init():
    try:
        with open("content.yml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        if not data:
            data = {}
    except Exception:
        data = {}
    return data


class Idea:
    def __init__(self) -> None:
        self.data = init()
        self.length = len(self.data)

    def add(self, idea):
        c = datetime.date.today()
        if not idea:
            return "please write some idea"
        try:
            ideas = self.data[c]
            if idea in ideas:
                return "already in your ideas !"
            else:
                self.data[c].append(idea)
        except:
            self.data[c] = [idea]
        save(self.data)

    def delete(self, day=None):
        self.data.pop(day, None)
        save(self.data)

    def show(self):
        i = 0
        for key in self.data.keys():
            print(Fore.YELLOW + "|", key, "|", Fore.WHITE)
            for idea in self.data[key]:
                i += 1
                paragraph = idea.split("  ")
                print("-", paragraph[0])
                try:
                    for j in range(1, len(paragraph)):
                        print(" ", paragraph[j])
                except:
                    pass
                if i == 20:
                    return

    def help(self):
        return """
        show : show all your ideas
        randshow : show ideas from a random day 
        quizzme : train your memory !
        add  : add an idea for today
        """

    def randshow(self):
        randkey = list(self.data.keys())
        randomk = randkey[random.randint(0, self.length - 1)]
        print(Fore.YELLOW + "|", randomk, "|", Fore.WHITE)
        for i in self.data[randomk]:
            print(i)

    def quizzme(self):
        print("beginning of the quizz !\n")
        time.sleep(2)
        for question, answer in self.data.items():
            score = 0
            for w in input(
                "Give me some ideas (separated by commas) from "
                + Fore.YELLOW
                + str(question)
                + Fore.WHITE
                + "\n->"
            ).split(","):
                for i in answer:
                    if similarity(w, i) > 0.5:
                        score += 1
                        break
            res = score / len(answer) * 100
            if res > 60:
                print(Fore.GREEN + str(res) + " %" + Fore.WHITE)
            else:
                print(Fore.YELLOW + str(res) + " %" + Fore.WHITE)


if __name__ == "__main__":
    fire.Fire(Idea())
