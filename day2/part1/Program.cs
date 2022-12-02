var lines = File.ReadAllLines("../input.txt");

// scores[mine][theirs]
int[][] scores = new int[][]
{
  new int[] { 3, 0, 6 }, // My choice Rock
  new int[] { 6, 3, 0 }, // My choice Paper
  new int[] { 0, 6, 3 }  // My choise Scissors
};

var decryptMove = (string move) =>
{
    switch (move)
    {
        case "A":
        case "X":
            return RpsMove.Rock;
        case "B":
        case "Y":
            return RpsMove.Paper;
        case "C":
        case "Z":
            return RpsMove.Scissors;
        default:
            throw new ArgumentException("Invalid value");
    }
};

var decodeLine = (string line) =>
{
    var moves = line.Split().Select(x => decryptMove(x)).ToArray();
    return new Round(moves[1], moves[0]);
};

var scoreRound = (Round round) =>
{
    var myMoveScore = (int)round.MyMove + 1;

    var outcomeScore = scores[(int)round.MyMove][(int)round.TheirMove];

    return myMoveScore + outcomeScore;
};

var totalScore = 0;

foreach (var line in lines)
{
    var round = decodeLine(line);
    totalScore += scoreRound(round);
}

Console.WriteLine(totalScore);

record Round(RpsMove MyMove, RpsMove TheirMove);

enum RpsMove
{
    Rock,
    Paper,
    Scissors
}