package main

import (
	"fmt"
	"io/ioutil"
	"strings"
	"unicode"
)

func main() {
	data, err := ioutil.ReadFile("input.txt")
	if err != nil {
		fmt.Println(err)
		return
	}

	input := string(data)
	allRucksacks := strings.Split(input, "\n")

	totalScore := 0

	groupItems := make(map[rune]int)
	for iteration, rucksackContents := range allRucksacks {
		uniqueItems := getUniqueItemsInRucksack(rucksackContents)

		for _, item := range uniqueItems {
			groupItems[item] += 1
		}

		if (iteration+1)%3 == 0 {
			for itemType, count := range groupItems {
				if count == 3 {
					totalScore += getScoreForItemType(itemType)
					break
				}
			}
			groupItems = make(map[rune]int)
		}
	}

	fmt.Println(totalScore)
}

func getUniqueItemsInRucksack(rucksackContents string) []rune {
	uniqueItemMap := make(map[rune]int)

	for _, itemType := range rucksackContents {
		uniqueItemMap[itemType] += 1
	}

	uniqueItems := make([]rune, len(uniqueItemMap))

	i := 0
	for k := range uniqueItemMap {
		uniqueItems[i] = k
		i++
	}

	return uniqueItems
}

func getScoreForItemType(itemType rune) int {
	score := 0
	if unicode.IsUpper(itemType) {
		score += 26
	}
	itemType = unicode.ToLower(itemType)

	score += int(itemType-'a') + 1

	return score
}
