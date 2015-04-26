#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def verifyStandings(correct_pairs, tournament):
    """helper methods"""
    pairings = swissPairings(tournament)
    num_pairs = len(correct_pairs)
    if len(pairings) != num_pairs:
        raise ValueError(
            "For {0} players, swissPairings should return {1} pairs.".format(num_pairs * 2, num_pairs))
    actual_pairs = set([frozenset([pid1, pid2]) for (pid1, pname1, pid2, pname2) in pairings])
    if correct_pairs != actual_pairs:
        print 'corrected pairs: {0}'.format(correct_pairs)
        print 'actual pairs: {0}'.format(actual_pairs)
        raise ValueError(
            "swissPairings result not matched with correct pairs")


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    c = countTournamentPlayers()
    if c == '0':
        raise TypeError(
            "countTournamentPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countTournamentPlayers should return zero.")
    print "3. After deleting, countPlayers() and countTournamentPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    tournament = registerTournament('Tourney of the Hand')
    p1 = registerPlayer("Melpomene Murray")
    p2 = registerPlayer("Randy Schwartz")
    registerTournamentPlayer(p1, tournament)
    registerTournamentPlayer(p2, tournament)
    standings = tournamentPlayerStandings(tournament)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    p1 = registerPlayer("Bruno Walton")
    p2 = registerPlayer("Boots O'Neal")
    p3 = registerPlayer("Cathy Burton")
    p4 = registerPlayer("Diane Grant")
    tournament = registerTournament('Tourney of the Hand')
    registerTournamentPlayer(p1, tournament)
    registerTournamentPlayer(p2, tournament)
    registerTournamentPlayer(p3, tournament)
    registerTournamentPlayer(p4, tournament)
    standings = tournamentPlayerStandings(tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament, id1, id2)
    reportMatch(tournament, id3, id4)
    standings = tournamentPlayerStandings(tournament)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    p1 = registerPlayer("Twilight Sparkle")
    p2 = registerPlayer("Fluttershy")
    p3 = registerPlayer("Applejack")
    p4 = registerPlayer("Pinkie Pie")
    tournament = registerTournament('Tourney of the Hand')
    registerTournamentPlayer(p1, tournament)
    registerTournamentPlayer(p2, tournament)
    registerTournamentPlayer(p3, tournament)
    registerTournamentPlayer(p4, tournament)
    standings = tournamentPlayerStandings(tournament)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournament, id1, id2)
    reportMatch(tournament, id3, id4)
    correct_pairs = set([frozenset([id1, id3]),
                         frozenset([id2, id4])])
    verifyStandings(correct_pairs, tournament)
    print "8. After one match, players with one win are paired."


def testMultipleTournaments():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    # players
    p1 = registerPlayer("Twilight Sparkle")
    p2 = registerPlayer("Fluttershy")
    p3 = registerPlayer("Applejack")
    p4 = registerPlayer("Pinkie Pie")
    p5 = registerPlayer("Gregor Clegane")
    p6 = registerPlayer("Loras Tyrell")
    # tournament 1
    t1 = registerTournament('Tourney of the Hand')
    registerTournamentPlayer(p1, t1)
    registerTournamentPlayer(p2, t1)
    registerTournamentPlayer(p3, t1)
    registerTournamentPlayer(p4, t1)
    standings = tournamentPlayerStandings(t1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    # t1 first round
    reportMatch(t1, id1, id2)
    reportMatch(t1, id3, id4)
    correct_pairs = set([frozenset([id1, id3]),
                         frozenset([id2, id4])])
    verifyStandings(correct_pairs, t1)
    # tournament 2
    t2 = registerTournament('King Joffrey\'s Nameday')
    registerTournamentPlayer(p5, t2)
    registerTournamentPlayer(p6, t2)
    registerTournamentPlayer(p3, t2)
    registerTournamentPlayer(p4, t2)
    standings = tournamentPlayerStandings(t2)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    # t2 first round
    reportMatch(t2, id1, id2)
    reportMatch(t2, id3, id4)
    correct_pairs = set([frozenset([id1, id3]),
                         frozenset([id2, id4])])
    verifyStandings(correct_pairs, t2)
    print "9. After one match, players with one win are paired in two different tournament"


def testComplicatedTournament():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    # players
    a = registerPlayer("A")
    b = registerPlayer("B")
    c = registerPlayer("C")
    d = registerPlayer("D")
    e = registerPlayer("E")
    f = registerPlayer("F")
    g = registerPlayer("G")
    h = registerPlayer("H")
    # tournament
    t1 = registerTournament('WrestleMania 31')
    registerTournamentPlayer(a, t1)
    registerTournamentPlayer(b, t1)
    registerTournamentPlayer(c, t1)
    registerTournamentPlayer(d, t1)
    registerTournamentPlayer(e, t1)
    registerTournamentPlayer(f, t1)
    registerTournamentPlayer(g, t1)
    registerTournamentPlayer(h, t1)
    standings = tournamentPlayerStandings(t1)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    # 1st round
    reportMatch(t1, id2, id1)
    reportMatch(t1, id3, id4)
    reportMatch(t1, id6, id5)
    reportMatch(t1, id7, id8)
    correct_pairs = set([frozenset([id2, id3]),
                         frozenset([id6, id7]),
                         frozenset([id1, id4]),
                         frozenset([id5, id8])])
    verifyStandings(correct_pairs, t1)
    # 2nd round
    reportMatch(t1, id3, id2)
    reportMatch(t1, id6, id7)
    reportMatch(t1, id4, id1)
    reportMatch(t1, id8, id5)
    correct_pairs = set([frozenset([id3, id6]),
                         frozenset([id7, id2]),
                         frozenset([id4, id8]),
                         frozenset([id1, id5])])
    verifyStandings(correct_pairs, t1)
    # 3rd round
    reportMatch(t1, id3, id6)
    reportMatch(t1, id2, id4)
    reportMatch(t1, id7, id8)
    reportMatch(t1, id5, id1)
    correct_pairs = set([frozenset([id3, id6]),
                         frozenset([id7, id2]),
                         frozenset([id8, id4]),
                         frozenset([id5, id1])])
    verifyStandings(correct_pairs, t1)
    print "10. After 3 rounds match, tournament should produce expected standings"


def testEvenMatches():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    # players
    a = registerPlayer("A")
    b = registerPlayer("B")
    c = registerPlayer("C")
    d = registerPlayer("D")
    e = registerPlayer("E")
    f = registerPlayer("F")
    g = registerPlayer("G")
    h = registerPlayer("H")
    # tournament
    t1 = registerTournament('Panda Express Cock Magic')
    registerTournamentPlayer(a, t1)
    registerTournamentPlayer(b, t1)
    registerTournamentPlayer(c, t1)
    registerTournamentPlayer(d, t1)
    registerTournamentPlayer(e, t1)
    registerTournamentPlayer(f, t1)
    registerTournamentPlayer(g, t1)
    registerTournamentPlayer(h, t1)
    standings = tournamentPlayerStandings(t1)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    # 1st round
    reportMatch(t1, id1, id2)
    reportTiedMatch(t1, id3, id4)
    reportTiedMatch(t1, id5, id6)
    reportMatch(t1, id7, id8)
    correct_pairs = set([frozenset([id1, id7]),
                         frozenset([id2, id3]),
                         frozenset([id4, id5]),
                         frozenset([id6, id8])])
    verifyStandings(correct_pairs, t1)
    print "11. With two tied mathces, players with one win should be paired"


def testForOddPlayersTournament():
    deleteMatches()
    deletePlayers()
    deleteTournamentPlayers()
    deleteTournaments()
    # players
    a = registerPlayer("1")
    b = registerPlayer("2")
    c = registerPlayer("3")
    # tournament
    t1 = registerTournament('Very Odd')
    registerTournamentPlayer(a, t1)
    registerTournamentPlayer(b, t1)
    registerTournamentPlayer(c, t1)
    standings = tournamentPlayerStandings(t1)
    [id1, id2, id3] = [row[0] for row in standings]
    # 1st round
    reportMatch(t1, id2, id1)
    reportByeMatch(id3)
    correct_pairs = set([frozenset([id2, 'bye']),
                         frozenset([id3, id1])])
    verifyStandings(correct_pairs, t1)
    print "12. with odd number of players, bye match is added"


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testMultipleTournaments()
    testComplicatedTournament()
    testEvenMatches()
    testForOddPlayersTournament()
    print "Success!  All tests pass!"
