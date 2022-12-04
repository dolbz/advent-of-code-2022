#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Range
{
  int start;
  int end;
};

const char *sectionSeperator = ",";
const char *rangeSeperator = "-";

struct Range extractRange(char *sectionRangeStr)
{
  char *rangeStart = strtok(sectionRangeStr, rangeSeperator);
  char *rangeEnd = strtok(NULL, rangeSeperator);

  struct Range range;
  range.start = atoi(rangeStart);
  range.end = atoi(rangeEnd);

  return range;
}

int main()
{
  FILE *file = fopen("input.txt", "r");

  if (file == NULL)
  {
    perror("Error opening file");
    return 1;
  }

  int fullyContainedPairs = 0;

  char line[256];
  while (fgets(line, sizeof(line), file))
  {
    char *firstSectionStr = strtok(line, sectionSeperator);
    char *secondSectionStr = strtok(NULL, sectionSeperator);

    struct Range firstSectionRange = extractRange(firstSectionStr);
    struct Range secondSectionRange = extractRange(secondSectionStr);

    if ((firstSectionRange.end >= secondSectionRange.start && firstSectionRange.start <= secondSectionRange.end) ||
        (secondSectionRange.end >= firstSectionRange.start && secondSectionRange.start <= firstSectionRange.end))
    {
      fullyContainedPairs++;
    }
  }

  fclose(file);

  printf("%d\n", fullyContainedPairs);

  return 0;
}