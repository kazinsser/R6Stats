#!/usr/bin/python3.4

import asyncio
import r6sapi as api
import configparser
import datetime
import time
from spreadsheet import GoogleSheet


class R6Stats:
    username = ""
    password = ""

    def get_credentials(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.username = config.get('uplay-login', 'username')
        self.password = config.get('uplay-login', 'password')

    @asyncio.coroutine
    def run(self):
        self.get_credentials()
        auth = api.Auth(self.username, self.password)

        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        print(date)
        weekday = now.weekday()

        players = ['Atsuraka', 'CarpeVexillumTV', 'jmsst110', 'Kazology', 'Madmaxdog1', 'Mcloov', 'CommanderCreem',
                   'SpartanBH', 'Spottykus', 'WM_Feedback']

        google_sheet = GoogleSheet()

        general_sheet = google_sheet.get_sheet('general_stats')

        if weekday == 6:
            weapon_sheet = google_sheet.get_sheet('weapon_stats')
            operator_sheet = google_sheet.get_sheet('operator_stats')
            gametype_sheet = google_sheet.get_sheet('gametype_stats')

        for name in players:
            try:
                player = yield from auth.get_player(name, api.Platforms.UPLAY)
            except api.r6sapi.InvalidRequest:
                continue

            general_stats = [name, date]
            weapon_stats = [name, date]
            operator_stats = [name, date]
            gametype_stats = [name, date]

            print(name, 'Complete Stats')

            if weekday == 6:
                weapons = yield from player.check_weapons()
                for w in weapons:
                    weapon_stats.append(w.kills)
                    weapon_stats.append(w.headshots)
                    weapon_stats.append(w.hits)
                    weapon_stats.append(w.shots)

                    print(w.name, 'Stats')
                    print('Kills:', w.kills)
                    print('Headshots:', w.headshots)
                    print('Hits:', w.hits)
                    print('Shots:', w.shots)
                    print('')

                operators = []
                attack_operators = ['Ash', 'Blitz', 'Blackbeard', 'Buck', 'Capitao', 'Fuze', 'Glaz', 'Hibana', 'IQ',
                                    'Jackal', 'Montagne', 'Sledge', 'Thatcher', 'Thermite', 'Twitch']
                defense_operators = ['Bandit', 'Castle', 'Caveira', 'Doc', 'Echo', 'Frost', 'Jager', 'Kapkan', 'Mira',
                                     'Mute', 'Pulse', 'Rook', 'Smoke', 'Tachanka', 'Valkyrie']

                operators.extend(attack_operators)
                operators.extend(defense_operators)

                for op_name in operators:
                    operator = yield from player.get_operator(op_name)

                    operator_stats.append(operator.kills)
                    operator_stats.append(operator.deaths)
                    operator_stats.append(operator.wins)
                    operator_stats.append(operator.losses)
                    operator_stats.append(operator.headshots)
                    operator_stats.append(operator.melees)
                    operator_stats.append(operator.dbnos)
                    operator_stats.append(str(round(operator.time_played/3600, 2)))
                    operator_stats.append(str(operator.statistic) + ' ' + operator.statistic_name)

                    print(op_name, 'Stats')
                    print('Kills:', operator.kills)
                    print('Deaths:', operator.deaths)
                    print('Wins:', operator.wins)
                    print('Losses:', operator.losses)
                    print('Headshots:', operator.headshots)
                    print('Melees:', operator.melees)
                    print('DBNOs:', operator.dbnos)
                    print('Time:', round(operator.time_played/3600, 2), 'hours')
                    print('Statistic:', operator.statistic, operator.statistic_name)
                    print('')

                gametypes = yield from player.check_gamemodes()
                for g in gametypes:
                    gtype = gametypes[g]

                    gametype_stats.append(gtype.played)
                    gametype_stats.append(gtype.won)
                    gametype_stats.append(gtype.lost)
                    gametype_stats.append(gtype.best_score)

                    print(gtype.name, 'Stats')
                    print('Played:', gtype.played)
                    print('Wins:', gtype.won)
                    print('Lost:', gtype.lost)
                    print('Best Score:', gtype.best_score)
                    print('')

            print('General Stats')
            yield from player.check_level()
            general_stats.append(player.level)
            general_stats.append(player.xp)

            print('Level:', player.level)
            print('XP:', player.xp)

            yield from player.check_general()
            general_stats.append(player.matches_played)
            general_stats.append(player.matches_won)
            general_stats.append(player.matches_lost)
            general_stats.append(player.kills)
            general_stats.append(player.deaths)
            general_stats.append(str(round(player.time_played/3600, 2)))
            general_stats.append(player.melee_kills)
            general_stats.append(player.kill_assists)
            general_stats.append(player.penetration_kills)
            general_stats.append(player.revives)
            general_stats.append(player.bullets_fired)
            general_stats.append(player.bullets_hit)
            general_stats.append(player.headshots)

            print('Played:', player.matches_played)
            print('Wins:', player.matches_won)
            print('Lost:', player.matches_lost)
            print('Kills:', player.kills)
            print('Deaths:', player.deaths)
            print('Time Played:', round(player.time_played / 3600, 2), 'hours')
            print('Melees:', player.melee_kills)
            print('Assists:', player.kill_assists)
            print('Penetrations:', player.penetration_kills)
            print('Revives:', player.revives)
            print('Bullets Fired:', player.bullets_fired)
            print('Bullets Hit:', player.bullets_hit)
            print('Headshots:', player.headshots)
            print('')

            yield from player.check_queues()

            casual = player.casual
            general_stats.append(casual.played)
            general_stats.append(casual.won)
            general_stats.append(casual.lost)
            general_stats.append(casual.kills)
            general_stats.append(casual.deaths)
            general_stats.append(str(round(casual.time_played/3600, 2)))

            print(casual.name.title(), 'Stats')
            print('Played:', casual.played)
            print('Wins:', casual.won)
            print('Lost:', casual.lost)
            print('Kills:', casual.kills)
            print('Deaths:', casual.deaths)
            print('Time Played:', round(casual.time_played/3600, 2), 'hours')
            print('')

            ranked = player.ranked
            general_stats.append(ranked.played)
            general_stats.append(ranked.won)
            general_stats.append(ranked.lost)
            general_stats.append(ranked.kills)
            general_stats.append(ranked.deaths)
            general_stats.append(str(round(ranked.time_played/3600, 2)))

            print(ranked.name.title(), 'Stats')
            print('Played:', ranked.played)
            print('Wins:', ranked.won)
            print('Lost:', ranked.lost)
            print('Kills:', ranked.kills)
            print('Deaths:', ranked.deaths)
            print('Time Played:', round(ranked.time_played/3600, 2), 'hours')
            print('')

            region = api.RankedRegions.NA
            season = yield from player.get_rank(region)

            general_stats.append(season.season)
            general_stats.append(str(int(season.mmr)))
            general_stats.append(str(int(season.max_mmr)))
            general_stats.append(str(round(season.skill_mean, 2)))
            general_stats.append(str(round(season.skill_stdev, 2)))

            print('Ranked Season Stats')
            print('Current Season:', season.season)
            print('Current MMR:', int(season.mmr))
            print('Max MMR:', int(season.max_mmr))
            print('Skill Mean:', round(season.skill_mean, 2))
            print('Standard Deviation:', round(season.skill_stdev, 2))
            print('')
            print('-----------------------------')
            print('')

            general_sheet.append_row(general_stats)

            if weekday == 6:
                weapon_sheet.append_row(weapon_stats)
                operator_sheet.append_row(operator_stats)
                gametype_sheet.append_row(gametype_stats)

            time.sleep(10)

        yield from auth.session.close()


main = R6Stats()

loop = asyncio.get_event_loop()
loop.run_until_complete(main.run())
