var lines = File.ReadAllLines("../input.txt");

// moveMatrix[theirMove][requiredOutcome]
RpsMove[][] moveMatrix = new RpsMove[][]
{
  new[] { RpsMove.Scissors, RpsMove.Rock, RpsMove.Paper }, // Their move Rock
  new[] { RpsMove.Rock, RpsMove.Paper, RpsMove.Scissors }, // Their move Paper
  new[] { RpsMove.Paper, RpsMove.Scissors, RpsMove.Rock }  // Their move Scissors
};

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
            return RpsMove.Rock;
        case "B":
            return RpsMove.Paper;
        case "C":
            return RpsMove.Scissors;
        default:
            throw new ArgumentException("Invalid value");
    }
};

var decryptResult = (string encodedResult) =>
{
    switch (encodedResult)
    {
        case "X":
            return RequiredOutcome.Lose;
        case "Y":
            return RequiredOutcome.Draw;
        case "Z":
            return RequiredOutcome.Win;
        default:
            throw new ArgumentException("Invalid value");
    }
};

var decodeLine = (string line) =>
{
    var parts = line.Split();
    var opponentMove = decryptMove(parts[0]);
    var requiredOutcome = decryptResult(parts[1]);

    var myMove = moveMatrix[(int)opponentMove][(int)requiredOutcome];

    return new Round(myMove, opponentMove);
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

enum RequiredOutcome
{
    Lose,
    Draw,
    Win
}

enum RpsMove
{
    Rock,
    Paper,
    Scissors
}