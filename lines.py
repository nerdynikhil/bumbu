import hashlib

LINES = [
    # hellos
    "hiii :3", "hello hello!", "oh hi! didn't see you there", "heyyy bestie",
    "i missed you!", "you're back!", "peekaboo!", "boop!",
    # pep talks
    "you're doing great!", "i believe in you!", "you've got this!", "so proud of you",
    "one step at a time", "you're smarter than you think", "look at you go!",
    "you make hard things look easy", "mistakes mean you're learning", "keep going, superstar",
    "today is your day", "you're unstoppable!", "tiny progress is still progress",
    "you're doing better than you think", "big brain moment!", "nailed it!",
    # self care
    "drink some water!", "take a tiny break?", "stretch your arms!", "roll your shoulders",
    "blink a few times for me", "have you eaten yet?", "snack time?", "deep breath in... and out",
    "don't forget to smile", "sit up straight, cutie", "go look out the window",
    "rest your eyes a little", "you deserve a treat", "be kind to yourself today",
    "it's okay to slow down", "a walk sounds nice", "bedtime soon?",
    # love and friendship
    "you're my favorite human", "wanna be friends?", "i like your cursor",
    "you have a great smile", "sending you a big hug", "you make my day",
    "i'm so lucky to have you", "you're super cool", "best human ever",
    "you're the cutest", "i'm always here for you", "you light up my screen",
    "you're my sunshine", "high five!", "virtual hug incoming!",
    # silly
    "*wiggles*", "uwu", "hehe", "i'm a little sleepy", "is it nap time?",
    "what are we working on?", "ooh, what's that?", "can i help?",
    "i'm chasing your cursor!", "wheee!", "i'm faster than you think",
    "catch me if you can!", "i saw a butterfly", "i love clouds",
    "do you like pancakes?", "i dreamed about cookies", "let's go on an adventure",
    "i'm practicing my dance moves", "tickle tickle!", "is this the internet?",
    "click click click", "so many tabs!", "ooh, shiny button",
    "i counted to ten! almost", "my favorite color is all of them",
    "i'm small but mighty", "do i look cute today?", "teehee",
    "i found a pixel!", "life is good", "la la la",
]
PET_LINES = {
    "Octopus": [
        "8 arms, all for hugs", "blub blub", "ink-credible work!", "i'm a squishy octopus",
        "the ocean says hi", "tentacle high five!", "i can hug eight things at once",
        "bubbles!", "you're o-fish-ally awesome", "sea you later? no, stay!",
        "i'm feeling a little pink today", "squish squish",
    ],
    "Cat": [
        "meow :3", "purr purr", "pet me pls", "i knocked something over",
        "is that a laser dot?", "nap on the keyboard?", "you're purr-fect",
        "feed me, human", "i'm not cute, i'm fierce", "mew!",
        "i sat in a box today", "chin scratches please",
    ],
    "Bunny": [
        "hop hop!", "got any carrots?", "*nose wiggle*", "some-bunny loves you",
        "my ears are listening", "hoppy day!", "i'm soft and fluffy",
        "you're hop-solutely amazing", "binky time!", "boing boing",
        "i'm ear for you", "carrot cake, please",
    ],
    "Duck": [
        "quack!", "quack quack <3", "you're un-duck-niably great", "waddle waddle",
        "i'm one lucky duck", "splish splash!", "got any bread?",
        "duck yeah!", "i'm quackers about you", "rubber duck debugging time",
        "puddles are the best", "honk! wait, that's geese",
    ],
    "Frog": [
        "ribbit!", "toad-ally proud of you", "hop to it!", "it's a good day to be a frog",
        "i caught a fly!", "lily pads are comfy", "you're ribbiting!",
        "croak croak", "i'm hoppy to see you", "rainy days are my favorite",
        "jump jump!", "i'm a little green bean",
    ],
}
VOICE = "en-US-AnaNeural"
# how to say lines that don't read well out loud
SPOKEN = {
    "hiii :3": "hiiii!", "*wiggles*": "wiggle wiggle!", "uwu": "oo woo!",
    "meow :3": "meow!", "*nose wiggle*": "sniff sniff!", "quack quack <3": "quack quack!",
    "pet me pls": "pet me please!", "hehe": "hee hee!", "teehee": "tee hee!",
    "honk! wait, that's geese": "honk! wait, that's geese.",
}


def sound_file(line):
    return hashlib.md5(line.encode()).hexdigest()[:10] + ".mp3"
