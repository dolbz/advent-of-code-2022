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

	for _, rucksackContents := range allRucksacks {
		totalItems := len(rucksackContents)

		itemsMap := make(map[rune]int)
		for i, itemChar := range rucksackContents {
			if i < totalItems/2 {
				itemsMap[itemChar] = 1
			} else if itemsMap[itemChar] != 0 {
				itemsMap[itemChar] = 2
			}
		}

		for itemType, presentInCompartments := range itemsMap {
			if presentInCompartments == 2 {
				totalScore += getScoreForItemType(itemType)
			}
		}
	}

	fmt.Println(totalScore)
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
