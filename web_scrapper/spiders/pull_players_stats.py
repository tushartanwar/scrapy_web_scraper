import scrapy
import re


class ToScrapePlayerStats(scrapy.Spider):
    name = 'pull_player_stats'
    with open('../out/players_url_list.out', 'r') as f:
        players_url_list = f.read().splitlines()
    start_urls = players_url_list

    def parse(self, response):

        for player in response.xpath('.'):
            player_info = {}
            player_id = player.xpath('.//div[@class="info"]/h1/text()').get().partition("(")[2].split(':')[1].replace(')','').strip()
            player_name = player.xpath('.//div[@class="info"]/h1/text()').get().partition("(")[0].strip()
            player_misc_dat = player.xpath('.//div[@class="info"]/div/text()').getall()[-1].strip()
            player_nationality = player.xpath('string(.//div[@class="info"]/div/a/@title)').get()
            player_weight = player_misc_dat.split()[-1]
            player_height = player_misc_dat.split()[-2]
            player_age = player_misc_dat.split()[1]
            player_photo_url = player.xpath('.//div[@class="bp3-card player"]//img/@data-src').get()
            preferred_foot = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-6"]//li[position()=1]/text()').getall()[
                1]
            international_reputation = player.xpath('.//div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-6"]//li[position()=2]/text()').getall()[1]
            weak_foot = player.xpath('.//div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-6"]//li[position()=3]/text()').getall()[1]
            skill_moves = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-6"]//li[position()=4]/text()').getall()[
                1]

            decider_string1 = player.xpath('string(.//div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"][1])').get()
            decider_string2 = player.xpath('string(.//div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"][2])').get()

            if 'joined' in str.lower(decider_string1) or 'loaned' in str.lower(decider_string1) or 'contract' in str.lower(decider_string1):
                country_index = '2'
                club_index = '1'
            elif 'joined' in str.lower(decider_string2) or 'loaned' in str.lower(decider_string2) or 'contract' in str.lower(decider_string2):
                country_index = '1'
                club_index = '2'
            elif 'joined' not in str.lower(decider_string1) and 'joined' not in str.lower(decider_string2) \
                    and 'loaned' not in str.lower(decider_string1) and 'loaned' not in str.lower(decider_string2) \
                    and 'contract' not in str.lower(decider_string1) and 'contract' not in str.lower(decider_string2) \
                    and 'jersey' in str.lower(decider_string2):
                country_index = '2'
                club_index = '1'
            else:
                country_index = '1'
                club_index = '2'

            club_flag_url = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+club_index+']//img/@data-src').get()
            club_name = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+club_index+']//li[position()=1]//a/text()').get()
            club_playing_position = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+club_index+']//li[position()=3]//span/text()').get()
            club_jersey_number = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+club_index+']//li[position()=4]/text()').get()
            current_club_joined_dt = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+club_index+']//li[position()=5]/text()').get()
            current_club_contract_valid_yr = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+club_index+']//li[position()=6]/text()').get()
            country = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+country_index+']//li[position()=1]//a/text()').get()
            country_flag_url = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+country_index+']//img/@data-src').get()
            country_playing_position = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+country_index+']//li[position()=3]//span/text()').get()
            country_jersey_number = player.xpath(
                './/div[@class="teams spacing"]/div[@class="columns"]//div[@class="column col-5"]['+country_index+']//li[position()=4]/text()').get()

            # Fetching high level attributes.
            high_level_attr = ['overall_rating', 'potential', 'value', 'wage']
            overall_attributes = {}
            for i in range(1, 5):
                overall_attributes.update({high_level_attr[i - 1]: player.xpath(
                    './/div[@class="bp3-callout"]/div[@class="columns"]/div[' + str(i) + ']//span/text()').get()})


            # Fetching rating for attacking, Skills, movement, power, mentality, defending, goalkeeping, traits
            attack_dict = {}
            skill_dict = {}
            movement_dict = {}
            power_dict = {}
            mentality_dict = {}
            defending_dict = {}
            goalkeeping_dict = {}
            
            for i in range(1, 7):
                try:
                    attack_list = player.xpath(
                        './/div[@class="bp3-card"]/div[@class="columns spacing"][1]/div[@class="column col-4"][1]//li[' + str(
                            i) + ']/span/text()').getall()
                    attack_dict.update({attack_list[1]: attack_list[0]})
                except:
                    pass
                try:
                    skill_list = player.xpath(
                        './/div[@class="bp3-card"]/div[@class="columns spacing"][1]/div[@class="column col-4"][2]//li[' + str(
                            i) + ']/span/text()').getall()
                    skill_dict.update({skill_list[1]: skill_list[0]})
                except:
                    pass
                try:
                    movement_list = player.xpath(
                        './/div[@class="bp3-card"]/div[@class="columns spacing"][1]/div[@class="column col-4"][3]//li[' + str(
                            i) + ']/span/text()').getall()
                    movement_dict.update({movement_list[1]: movement_list[0]})
                except:
                    pass
                try:
                    power_list = player.xpath(
                        './/div[@class="bp3-card"]/div[@class="columns spacing"][1]/div[@class="column col-4"][4]//li[' + str(
                            i) + ']/span/text()').getall()
                    power_dict.update({power_list[1]: power_list[0]})
                except:
                    pass
                try:
                    mentality_list = player.xpath(
                        './/div[@class="bp3-card"]/div[@class="columns spacing"][2]/div[@class="column col-4"][1]//li[' + str(
                            i) + ']/span/text()').getall()
                    mentality_dict.update({mentality_list[1]: mentality_list[0]})
                except:
                    pass
                try:
                    defending_list = player.xpath(
                        './/div[@class="bp3-card"]/div[@class="columns spacing"][2]/div[@class="column col-4"][2]//li[' + str(
                            i) + ']/span/text()').getall()
                    defending_dict.update({defending_list[1]: defending_list[0]})
                except:
                    pass
                try:
                    goalkeeping_list = player.xpath(
                        './/div[@class="bp3-card"]/div[@class="columns spacing"][2]/div[@class="column col-4"][3]//li[' + str(
                            i) + ']//text()').getall()
                    goalkeeping_dict.update({goalkeeping_list[1]: goalkeeping_list[0]})
                except:
                    pass

            real_rating_dict = {}
            for x in range(1, 7):
                raw_real_rating = player.xpath(
                    './/div[@class="center"]//aside//div[@class="bp3-callout spacing calculated"]/div[@class="columns"][' + str(
                        x) + ']//div/text()').getall()
                special_elements = [x for x in raw_real_rating if not bool(re.match('^[a-zA-Z0-9\+]+$', x))]
                real_rating_list = [x for x in raw_real_rating if x not in special_elements]
                real_rating_dict.update(zip(real_rating_list[0::2], real_rating_list[1::2]))

            player_info = {}
            player_info.update({'player_id': player_id,
                                'player_name': player_name,
                                'player_weight':player_weight,
                                'player_height':player_height,
                                'player_nationality':player_nationality,
                                'player_age':player_age,
                                'player_photo_url': player_photo_url,
                                'preferred_foot': preferred_foot,
                                'club_flag_url': club_flag_url,
                                'club_name': club_name,
                                'club_playing_position': club_playing_position,
                                'club_jersey_number': club_jersey_number,
                                'current_club_joined_dt': current_club_joined_dt,
                                'current_club_contract_valid_yr': current_club_contract_valid_yr,
                                'country': country,
                                'country_flag_url': country_flag_url,
                                'country_playing_position': country_playing_position,
                                'country_jersey_number': country_jersey_number,
                                'international_reputation': international_reputation,
                                'weak_foot': weak_foot,
                                'skill_moves': skill_moves
                                })
            player_info.update(overall_attributes)
            player_info.update(attack_dict)
            player_info.update(skill_dict)
            player_info.update(movement_dict)
            player_info.update(power_dict)
            player_info.update(mentality_dict)
            player_info.update(defending_dict)
            player_info.update(goalkeeping_dict)
            player_info.update(real_rating_dict)


            yield player_info