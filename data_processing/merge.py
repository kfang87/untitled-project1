# -*- coding: utf-8 -*-

__author__ = 'Kayla'
from data_processing.untitledutils import  merge_persons
import logging, logging.config

def merge_all():

    # Ron Weasley
    # merge_persons('ron-weasley_harry-potter-and-the-chamber-of-secrets','ron-weasley','Ronald Weasley','Harry Potter series')
    # merge_persons('ron-weasley_harry-potter-and-the-prisoner-of-azkaban','ron-weasley','Ronald Weasley','Harry Potter series')
    # merge_persons('ron-weasley_harry-potter-and-the-goblet-of-fire','ron-weasley','Ronald Weasley','Harry Potter series')
    # merge_persons('ron-weasley_harry-potter-and-the-deathly-hallows','ron-weasley','Ronald Weasley','Harry Potter series')
    # merge_persons("harry-potter_harry-potter-and-the-chamber-of-secrets", "harry-potter","Harry Potter","Harry Potter Series")
    # merge_persons("harry-potter_harry-potter-and-the-deathly-hallows", "harry-potter","Harry Potter","Harry Potter Series")
    # merge_persons("harry-potter_harry-potter-and-the-goblet-of-fire", "harry-potter","Harry Potter","Harry Potter Series")
    # merge_persons("harry-potter_harry-potter-and-the-halfblood-prince", "harry-potter","Harry Potter","Harry Potter Series")
    # merge_persons("harry-potter_harry-potter-and-the-order-of-the-phoenix", "harry-potter","Harry Potter","Harry Potter Series")
    # merge_persons("harry-potter_harry-potter-and-the-prisoner-of-azkaban", "harry-potter","Harry Potter","Harry Potter Series")
    # merge_persons("harry-potter_harry-potter-and-the-sorcerer’s-stone", "harry-potter","Harry Potter","Harry Potter Series")
    # merge_persons("hermione-granger_harry-potter-and-the-chamber-of-secrets", "hermione-granger","Hermione Granger","Harry Potter Series")
    # merge_persons("hermione-granger_harry-potter-and-the-goblet-of-fire", "hermione-granger","Hermione Granger","Harry Potter Series")
    # merge_persons("hermione-granger_harry-potter-and-the-prisoner-of-azkaban", "hermione-granger","Hermione Granger","Harry Potter Series")
    # merge_persons("hermione-granger_harry-potter-and-the-sorcerer’s-stone", "hermione-granger","Hermione Granger","Harry Potter Series")
    # merge_persons("ron-weasley_harry-potter-and-the-chamber-of-secrets", "ron-weasley","Ron Weasley","Harry Potter Series")
    # merge_persons("ron-weasley_harry-potter-and-the-deathly-hallows", "ron-weasley","Ron Weasley","Harry Potter Series")
    # merge_persons("ron-weasley_harry-potter-and-the-goblet-of-fire", "ron-weasley","Ron Weasley","Harry Potter Series")
    # merge_persons("ron-weasley_harry-potter-and-the-prisoner-of-azkaban", "ron-weasley","Ron Weasley","Harry Potter Series")
    # merge_persons("severus-snape_harry-potter-and-the-deathly-hallows", "severus-snape","Severus Snape","Harry Potter Series")
    # merge_persons("severus-snape_harry-potter-and-the-halfblood-prince", "severus-snape","Severus Snape","Harry Potter Series")
    # merge_persons("haymitch-abernathy_catching-fire", "haymitch-abernathy","Haymitch Abernathy","Hunger Games Trilogy")
    # merge_persons("haymitch-abernathy_the-hunger-games", "haymitch-abernathy","Haymitch Abernathy","Hunger Games Trilogy")
    # merge_persons("katniss-everdeen_catching-fire", "katniss-everdeen","Katniss Everdeen","Hunger Games Trilogy")
    # merge_persons("katniss-everdeen_the-hunger-games", "katniss-everdeen","Katniss Everdeen","Hunger Games Trilogy")
    # merge_persons("alice_alice’s-adventures-in-wonderland", "alice-liddell","Alice Liddell","Alice's Adventures")
    # merge_persons("alice_through-the-lookingglass", "alice-liddell","Alice Liddell","Alice's Adventures")
    # merge_persons("antigone_antigone", "antigone","Antigone","Greek Plays (Antigone et al)")
    # merge_persons("antigone_the-oedipus-plays", "antigone","Antigone","Greek Plays (Antigone et al)")
    # merge_persons("gandalf_the-hobbit", "gandalf","Gandalf","Tolkien's Middle Earth")
    # merge_persons("gandalf-the-grey_the-fellowship-of-the-ring", "gandalf","Gandalf","Tolkien's Middle Earth")
    # merge_persons("gandalf-the-white_the-return-of-the-king", "gandalf","Gandalf","Tolkien's Middle Earth")
    # merge_persons("gandalf-the-white_the-two-towers", "gandalf","Gandalf","Tolkien's Middle Earth")
    # merge_persons("frodo-baggins_the-fellowship-of-the-ring", "frodo-baggins","Frodo Baggins","Tolkien's Middle Earth")
    # merge_persons("frodo-baggins_the-return-of-the-king", "frodo-baggins","Frodo Baggins","Tolkien's Middle Earth")
    # merge_persons("frodo-baggins_the-two-towers", "frodo-baggins","Frodo Baggins","Tolkien's Middle Earth")
    # merge_persons("sam-gamgee_the-fellowship-of-the-ring", "sam-gamgee","Sam Gamgee","Tolkien's Middle Earth")
    # merge_persons("sam-gamgee_the-return-of-the-king", "sam-gamgee","Sam Gamgee","Tolkien's Middle Earth")
    # merge_persons("sam-gamgee_the-two-towers", "sam-gamgee","Sam Gamgee","Tolkien's Middle Earth")
    # merge_persons("odysseus_mythology", "odysseus","Odysseus","Greek mythology (the Odyssey et al)")
    # merge_persons("odysseus_the-odyssey", "odysseus","Odysseus","Greek mythology (the Odyssey et al)")
    # merge_persons("oedipus_mythology", "oedipus","Oedipus","Greek plays (Oedipus the King et al)")
    # merge_persons("oedipus_the-oedipus-plays", "oedipus","Oedipus","Greek plays (Oedipus the King et al)")
    # merge_persons("peeta-mellark_catching-fire", "peeta-mellark","Peeta Mellark","Hunger Games Trilogy")
    # merge_persons("peeta-mellark_the-hunger-games", "peeta-mellark","Peeta Mellark","Hunger Games Trilogy")
    # merge_persons("sherlock-holmes_hound-of-the-baskervilles", "sherlock-holmes","Sherlock Holmes","Sherlock Holmes mysteries")
    # merge_persons("sherlock-holmes_the-redheaded-league", "sherlock-holmes","Sherlock Holmes","Sherlock Holmes mysteries")
    # merge_persons("tom-sawyer_the-adventures-of-huckleberry-finn", "tom-sawyer","Tom Sawyer","Mark Twain novels (The Adventures of Tom Sawyer et al)")
    # merge_persons("tom-sawyer_the-adventures-of-tom-sawyer", "tom-sawyer","Tom Sawyer","Mark Twain novels (The Adventures of Tom Sawyer et al)")
    # merge_persons("huck-finn_the-adventures-of-huckleberry-finn", "huckleberry-finn","Huckleberry Finn","Mark Twain novels (The Adventures of Huckleberry Finn et al)")
    # merge_persons("huckleberry-finn_the-adventures-of-tom-sawyer", "huckleberry-finn","Huckleberry Finn","Mark Twain novels (The Adventures of Huckleberry Finn et al)")
    # merge_persons("tyrion-lannister_a-clash-of-kings", "tyrion-lannister","Tyrion Lannister","Game of Thrones series")
    # merge_persons("tyrion-lannister_a-game-of-thrones", "tyrion-lannister","Tyrion Lannister","Game of Thrones series")
    # merge_persons("tyrion-lannister_a-storm-of-swords", "tyrion-lannister","Tyrion Lannister","Game of Thrones series")
    # merge_persons("tyurin_one-day-in-the-life-of-ivan-denisovich", "tyrion-lannister","Tyrion Lannister","Game of Thrones series")
    # merge_persons("arya-stark_a-clash-of-kings", "arya-stark","Arya Stark","Game of Thrones series")
    # merge_persons("arya-stark_a-storm-of-swords", "arya-stark","Arya Stark","Game of Thrones series")
    merge_persons("the-narrator_the-little-prince","the-narrator","The Narrator")
logging.config.fileConfig('logging.ini')
logger = logging.getLogger('root')
logger.info('Logging Started.')
merge_all()