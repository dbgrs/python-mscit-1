#paragraph = str(input("Enter text :"))

p = "The university was founded on 18 October 1920 as a 'Rashtriya Vidyapith' ('National University') by Mahatma Gandhi, who would serve throughout his life as the kulpati (chancellor) and all needs of Fund collected by sardar Vallabhbhai Patel by his personal relations and capacity."

words = []
duplicate = []

words=p.split()


print("Total Number of words:", len(words))
print("Uniqe words :",len(set(words)))
print("Longest : ", max(words, key=len))
print("Shortest : ", min(words, key=len))



for i in words:
    if(words.count(i) > 1):
        if(i not in duplicate):
            duplicate.append(i);
print("Word appearing more than word : ", duplicate)