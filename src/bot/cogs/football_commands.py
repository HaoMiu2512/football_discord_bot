import discord
from discord.ext import commands
import datetime

class FootballCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if hasattr(self.bot, 'notification_channel_id') and self.bot.notification_channel_id:
            if ctx.channel.id != self.bot.notification_channel_id:
                await ctx.send(f"⚠️ Bot chỉ hoạt động trong kênh <#{self.bot.notification_channel_id}>.", delete_after=5, ephemeral=True)
                return False
        return True

    @commands.hybrid_command(name='live', help='Hiển thị các trận đấu đang diễn ra')
    async def live_matches(self, ctx):
        await ctx.defer()
        
        matches = await self.bot.football_api.get_live_matches()
        if not matches:
            await ctx.send("Hiện không có trận đấu nào đang diễn ra trực tiếp.")
            return

        embed = discord.Embed(title="🔴 Các trận đấu đang diễn ra (LIVE)", color=discord.Color.red())
        for match in matches:
            home = match.get('homeTeam', {}).get('name', 'Home')
            away = match.get('awayTeam', {}).get('name', 'Away')
            
            score = match.get('score', {})
            full_time = score.get('fullTime', {})
            score_h = full_time.get('home')
            score_a = full_time.get('away')
            
            if score_h is None: score_h = 0
            if score_a is None: score_a = 0

            league = match.get('competition', {}).get('name', 'Unknown League')
            
            embed.add_field(
                name=f"{home} vs {away}",
                value=f"Giải: {league}\n**{score_h} - {score_a}**",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='matches', aliases=['scheduled'], help='Lịch thi đấu sắp tới')
    async def scheduled_matches(self, ctx):
        await ctx.defer()
        matches = await self.bot.football_api.get_scheduled_matches()
        if not matches:
            await ctx.send("Không tìm thấy trận đấu nào sắp tới (đang có trạng thái SCHEDULED).")
            return

        matches_to_show = matches[:10] 
        count = len(matches)

        embed = discord.Embed(title="📅 Lịch thi đấu sắp tới", description=f"Tìm thấy {count} trận. Hiển thị 10 trận đầu tiên.", color=discord.Color.blue())
        for match in matches_to_show:
            home = match.get('homeTeam', {}).get('name', 'Home')
            away = match.get('awayTeam', {}).get('name', 'Away')
            utc_date = match.get('utcDate', '')
            time_str = utc_date.split('T')[1][:5] if 'T' in utc_date else utc_date
            league = match.get('competition', {}).get('name', 'Unknown League')

            embed.add_field(
                name=f"{home} vs {away}",
                value=f"Giải: {league} | ⏰ {time_str} UTC",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='results', help='Kết quả các trận đấu đã kết thúc gần đây')
    async def finished_matches(self, ctx):
        await ctx.defer()
        matches = await self.bot.football_api.get_finished_matches()
        if not matches:
            await ctx.send("Không tìm thấy trận đấu nào đã kết thúc (gần đây).")
            return

        matches_to_show = matches[:10]
        count = len(matches)

        embed = discord.Embed(title="🏁 Kết quả trận đấu", description=f"Tìm thấy {count} trận. Hiển thị 10 trận đầu tiên.", color=discord.Color.dark_grey())
        for match in matches_to_show:
            home = match.get('homeTeam', {}).get('name', 'Home')
            away = match.get('awayTeam', {}).get('name', 'Away')
            
            score = match.get('score', {})
            full_time = score.get('fullTime', {})
            score_h = full_time.get('home', 0)
            score_a = full_time.get('away', 0)
            
            league = match.get('competition', {}).get('name', 'Unknown League')
            
            embed.add_field(
                name=f"{home} vs {away}",
                value=f"Giải: {league}\n**FT: {score_h} - {score_a}**",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='leagues', help='Danh sách các giải đấu hỗ trợ và mã (Code)')
    async def leagues(self, ctx):
        await ctx.defer()
        competitions = await self.bot.football_api.get_competitions()
        if not competitions:
            await ctx.send("Không lấy được danh sách giải đấu.")
            return

        embed = discord.Embed(title="🏆 Danh sách giải đấu", color=discord.Color.gold())
        description = ""
        for comp in competitions:
            name = comp.get('name')
            code = comp.get('code')
            if code:
                description += f"**{name}**: `{code}`\n"
        
        embed.description = description
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='standings', help='Xem bảng xếp hạng. Ví dụ: /standings PL')
    async def standings(self, ctx, league_code: str):
        await ctx.defer()
        league_code = league_code.upper()
        data = await self.bot.football_api.get_standings(league_code)
        
        if not data:
            await ctx.send(f"Không tìm thấy bảng xếp hạng cho mã: {league_code}. Hãy dùng `/leagues` để xem mã đúng.")
            return

        standing_table = None
        for table in data:
            if table.get('type') == 'TOTAL':
                standing_table = table.get('table', [])
                break
        
        if not standing_table:
            if len(data) > 0:
                standing_table = data[0].get('table', [])

        if not standing_table:
            await ctx.send("Không có dữ liệu bảng xếp hạng chi tiết.")
            return

        embed = discord.Embed(title=f"📊 Bảng xếp hạng: {league_code}", color=discord.Color.blue())
        
        table_text = ""
        for team in standing_table[:10]: 
            pos = team.get('position')
            name = team.get('team', {}).get('name')
            points = team.get('points')
            played = team.get('playedGames')
            goal_diff = team.get('goalDifference')
            table_text += f"`{pos}.` **{name}** | P: {played} | GD: {goal_diff} | **Pts: {points}**\n"

        embed.description = table_text
        embed.set_footer(text="Hiển thị Top 10 đội.")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='scorers', help='Xem vua phá lưới. Ví dụ: /scorers PL')
    async def top_scorers(self, ctx, league_code: str):
        await ctx.defer()
        league_code = league_code.upper()
        scorers = await self.bot.football_api.get_top_scorers(league_code)
        
        if not scorers:
            await ctx.send(f"Không lấy được danh sách vua phá lưới cho mã: {league_code}.")
            return

        embed = discord.Embed(title=f"👟 Vua phá lưới: {league_code}", color=discord.Color.purple())
        
        text = ""
        for player_data in scorers[:10]:
            name = player_data.get('player', {}).get('name')
            goals = player_data.get('goals')
            team = player_data.get('team', {}).get('name')
            text += f"**{name}** ({team}): {goals} bàn\n"
            
        embed.description = text
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='areas', help='Xem danh sách khu vực (Quốc gia/Vùng). Top 15.')
    async def areas(self, ctx):
        await ctx.defer()
        areas = await self.bot.football_api.get_areas()
        if not areas:
            await ctx.send("Không lấy được danh sách khu vực.")
            return

        embed = discord.Embed(title="🌍 Khu vực bóng đá (Top 15)", description="Danh sách các quốc gia/khu vực hỗ trợ.", color=discord.Color.teal())
        
        text = ""
        count = 0
        for area in areas:
            if count >= 15: break
            name = area.get('name')
            area_id = area.get('id')
            country_code = area.get('countryCode', '')
            text += f"**{name}** ({country_code}) - ID: `{area_id}`\n"
            count += 1
            
        embed.description = text
        embed.set_footer(text="Dùng ID khu vực để tra cứu chi tiết nếu cần.")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='teams', help='Xem danh sách đội bóng trong 1 giải. Ví dụ: /teams PL')
    async def teams(self, ctx, league_code: str):
        await ctx.defer()
        league_code = league_code.upper()
        teams = await self.bot.football_api.get_teams_in_competition(league_code)
        
        if not teams:
            await ctx.send(f"Không tìm thấy đội bóng nào cho giải: {league_code}.")
            return

        embed = discord.Embed(title=f"🛡️ Các đội bóng giải: {league_code}", color=discord.Color.dark_green())
        
        text = ""
        for team in teams:
            name = team.get('name')
            tla = team.get('tla', '') 
            team_id = team.get('id')
            text += f"**{name}** ({tla}) - ID: `{team_id}`\n"
            
        if len(text) > 4000:
            text = text[:4000] + "\n... (danh sách quá dài)"
            
        embed.description = text
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='team', help='Xem thông tin chi tiết đội bóng bằng ID. Ví dụ: /team 65 (Man City)')
    async def team_info(self, ctx, team_id: int):
        await ctx.defer()
        team = await self.bot.football_api.get_team(team_id)
        
        if not team:
            await ctx.send(f"Không tìm thấy thông tin đội bóng có ID: {team_id}.")
            return

        name = team.get('name')
        short_name = team.get('shortName')
        founded = team.get('founded')
        venue = team.get('venue')
        website = team.get('website')
        coach = team.get('coach', {}).get('name', 'N/A')
        
        embed = discord.Embed(title=f"🛡️ {name} ({short_name})", url=website, color=discord.Color.blue())
        if team.get('crest'):
            embed.set_thumbnail(url=team.get('crest'))
            
        embed.add_field(name="Thành lập", value=str(founded), inline=True)
        embed.add_field(name="Sân vận động", value=venue, inline=True)
        embed.add_field(name="HLV Trưởng", value=coach, inline=False)
        
        squad = team.get('squad', [])
        if squad:
            squad_text = ""
            for player in squad[:10]:
                p_name = player.get('name')
                p_pos = player.get('position')
                p_id = player.get('id')
                squad_text += f"**{p_name}** ({p_pos}) - ID: `{p_id}`\n"
            if len(squad) > 10:
                squad_text += f"... và {len(squad)-10} cầu thủ khác."
            
            embed.add_field(name="Đội hình (Top 10)", value=squad_text, inline=False)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='person', help='Xem thông tin cá nhân (Cầu thủ/HLV) bằng ID. Ví dụ: /person 44')
    async def person_info(self, ctx, person_id: int):
        await ctx.defer()
        person = await self.bot.football_api.get_person(person_id)
        
        if not person:
            await ctx.send(f"Không tìm thấy thông tin người có ID: {person_id}.")
            return

        name = person.get('name')
        nationality = person.get('nationality')
        position = person.get('position')
        dob = person.get('dateOfBirth')
        current_team = person.get('currentTeam', {}).get('name', 'Free Agent')
        
        embed = discord.Embed(title=f"👤 {name}", color=discord.Color.orange())
        embed.add_field(name="Quốc tịch", value=nationality, inline=True)
        embed.add_field(name="Vị trí", value=position, inline=True)
        embed.add_field(name="Ngày sinh", value=dob, inline=True)
        embed.add_field(name="CLB hiện tại", value=current_team, inline=False)
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='match', help='Xem chi tiết trận đấu bằng ID. Ví dụ: /match 12345')
    async def match_detail(self, ctx, match_id: int):
        await ctx.defer()
        match = await self.bot.football_api.get_match_by_id(match_id)
        
        if not match:
            await ctx.send(f"Không tìm thấy trận đấu có ID: {match_id}.")
            return

        home = match.get('homeTeam', {})
        away = match.get('awayTeam', {})
        score = match.get('score', {})
        full_time = score.get('fullTime', {})
        status = match.get('status')
        utc_date = match.get('utcDate')
        venue = match.get('venue', 'N/A')
        competition = match.get('competition', {}).get('name', 'Giải đấu')
        
        score_str = f"{full_time.get('home', 0)} - {full_time.get('away', 0)}"
        time_str = utc_date.split('T')[1][:5] if 'T' in utc_date else utc_date
        
        color = discord.Color.green() if status == 'LIVE' else discord.Color.blue()
        
        embed = discord.Embed(title=f"{home.get('name')} vs {away.get('name')}", description=f"{competition} - {status}", color=color)
        if match.get('competition', {}).get('emblem'):
            embed.set_thumbnail(url=match.get('competition', {}).get('emblem'))

        embed.add_field(name="⏱️ Thời gian", value=f"{time_str} (UTC)", inline=True)
        embed.add_field(name="🏟️ Sân vận động", value=venue, inline=True)
        embed.add_field(name="⚽ Tỉ số", value=score_str, inline=False)
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='today', help='Xem toàn bộ trận đấu hôm nay (Gọn)')
    async def today_matches(self, ctx):
        await ctx.defer()
        today_date = datetime.date.today().isoformat()
        
        matches = await self.bot.football_api.get_matches(dateFrom=today_date, dateTo=today_date)
        
        if not matches:
            await ctx.send("Hôm nay không có trận đấu nào.")
            return

        competitions = {}
        for match in matches:
            comp_name = match.get('competition', {}).get('name', 'Khác')
            if comp_name not in competitions:
                competitions[comp_name] = []
            competitions[comp_name].append(match)

        embed = discord.Embed(title=f"📅 Lịch thi đấu hôm nay ({today_date})", color=discord.Color.gold())
        
        count = 0
        for comp_name, match_list in competitions.items():
            if count >= 20: 
                embed.add_field(name="...", value="Còn nhiều giải khác...", inline=False)
                break
                
            field_value = ""
            for m in match_list:
                home = m.get('homeTeam', {}).get('tla', m.get('homeTeam', {}).get('shortName', 'Home'))
                away = m.get('awayTeam', {}).get('tla', m.get('awayTeam', {}).get('shortName', 'Away'))
                utc_date = m.get('utcDate')
                time_str = utc_date.split('T')[1][:5] if 'T' in utc_date else utc_date
                status = m.get('status')
                
                icon = "⏰"
                if status == 'FINISHED': icon = "🏁"
                elif status in ['LIVE', 'IN_PLAY', 'PAUSED']: icon = "🔴"
                
                score_info = ""
                if status in ['FINISHED', 'IN_PLAY', 'PAUSED']:
                    s_h = m.get('score', {}).get('fullTime', {}).get('home', 0)
                    s_a = m.get('score', {}).get('fullTime', {}).get('away', 0)
                    score_info = f" **{s_h}-{s_a}**"

                row = f"{icon} `{time_str}` **{home}** vs **{away}**{score_info} (`{m.get('id')}`)\n"
                
                if len(field_value) + len(row) > 1024:
                    field_value += "... + more\n"
                    break
                field_value += row
            
            if field_value:
                embed.add_field(name=f"🏆 {comp_name}", value=field_value, inline=False)
                count += 1

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='team-next', help='Trận tiếp theo của đội bóng. Ví dụ: /team-next 65')
    async def team_next(self, ctx, team_id: int):
        await ctx.defer()
        matches = await self.bot.football_api.get_team_matches(team_id, status='SCHEDULED')
        
        if not matches:
            await ctx.send(f"Không tìm thấy trận đấu sắp tới nào cho đội ID: {team_id}.")
            return

        matches.sort(key=lambda x: x['utcDate'])
        match = matches[0]
        await self.send_brief_match_info(ctx, match, "🔜 Trận đấu tiếp theo")

    @commands.hybrid_command(name='team-last', help='Trận gần nhất của đội bóng. Ví dụ: /team-last 65')
    async def team_last(self, ctx, team_id: int):
        await ctx.defer()
        matches = await self.bot.football_api.get_team_matches(team_id, status='FINISHED')
        
        if not matches:
            await ctx.send(f"Không tìm thấy trận đấu đã đấu nào cho đội ID: {team_id}.")
            return

        matches.sort(key=lambda x: x['utcDate']) 
        match = matches[-1]
        
        await self.send_brief_match_info(ctx, match, "🔙 Trận đấu gần nhất")

    async def send_brief_match_info(self, ctx, match, title_prefix):
        home = match.get('homeTeam', {}).get('name')
        away = match.get('awayTeam', {}).get('name')
        utc_date = match.get('utcDate')
        time_str = utc_date.split('T')[1][:5] if 'T' in utc_date else utc_date
        date_str = utc_date.split('T')[0] if 'T' in utc_date else utc_date
        competition = match.get('competition', {}).get('name')
        
        score_info = ""
        status = match.get('status')
        if status == 'FINISHED':
            s_h = match.get('score', {}).get('fullTime', {}).get('home', 0)
            s_a = match.get('score', {}).get('fullTime', {}).get('away', 0)
            score_info = f"\n**Tỉ số FT**: {s_h} - {s_a}"
        
        embed = discord.Embed(title=f"{title_prefix}: {home} vs {away}", description=f"🏆 {competition}", color=discord.Color.blue())
        embed.add_field(name="Thời gian", value=f"{date_str} lúc {time_str} (UTC)", inline=True)
        if score_info:
            embed.add_field(name="Kết quả", value=score_info, inline=True)
        
        embed.set_footer(text=f"ID trận đấu: {match.get('id')}")
        await ctx.send(embed=embed)

    @commands.command(name='sync', help='Đồng bộ lệnh slash (Admin only)')
    async def sync(self, ctx):
        async with ctx.typing():
            try:
                self.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
                await ctx.send(f"✅ Đã đồng bộ {len(synced)} lệnh slash slash cho server này! Bạn hãy thử gõ `/` lại nhé.")
            except Exception as e:
                await ctx.send(f"❌ Lỗi đồng bộ: {e}")

    @commands.hybrid_command(name='help', help='Hiển thị danh sách các lệnh hỗ trợ')
    async def help(self, ctx):
        embed = discord.Embed(
            title="🤖 Hướng dẫn sử dụng Football Bot",
            description="Dưới đây là danh sách các lệnh bạn có thể sử dụng:",
            color=discord.Color.green()
        )
        
        commands_list = [
            ("⚽ `/live`", "Xem các trận đấu đang diễn ra trực tiếp."),
            ("📅 `/today`", "Xem lịch thi đấu/kết quả hôm nay."),
            ("🔜 `/team-next [id]`", "Xem trận tiếp theo của đội."),
            ("🔙 `/team-last [id]`", "Xem trận gần nhất của đội."),
            ("🏁 `/results`", "Xem kết quả các trận đấu vừa kết thúc."),
            ("🏆 `/leagues`", "Xem danh sách và mã (Code) các giải đấu."),
            ("📊 `/standings [mã]`", "Xem bảng xếp hạng. VD: `/standings PL`"),
            ("👟 `/scorers [mã]`", "Xem vua phá lưới. VD: `/scorers PL`"),
            ("🛡️ `/teams [mã]`", "Xem các đội trong giải. VD: `/teams PL`"),
            ("ℹ️ `/team [id]`", "Xem chi tiết đội. VD: `/team 65`"),
            ("👤 `/person [id]`", "Xem thông tin người. VD: `/person 44`"),
            ("🔎 `/match [id]`", "Xem chi tiết trận đấu."),
            ("✨ `/areas`", "Xem danh sách khu vực."),
            ("🔄 `!sync`", "Đồng bộ lệnh mới."),
        ]

        for name, desc in commands_list:
            embed.add_field(name=name, value=desc, inline=False)
            
        embed.set_footer(text="Bot được tạo bởi API bóng đá miễn phí.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FootballCommands(bot))
