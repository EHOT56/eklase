from eklase import EklaseClientSession, LoginData
from datetime import datetime, timedelta
import asyncio


async def main():
    login_data = LoginData("eklase_login", "eklase_password") 
    async with EklaseClientSession(login_data) as eklase_client: # Es neesmu pārliecināts, ka tas derēs skolotājiem e-klasē
        get_weekly_journals_tasks = []
        get_weekly_journals_tasks.append(asyncio.create_task(eklase_client.journal_manager.get_weekly_journal(datetime.now())))

        check_weeks_ahead = 10
        for i in range(1, check_weeks_ahead+1):
            get_weekly_journals_tasks.append(asyncio.create_task(eklase_client.journal_manager.get_weekly_journal(datetime.now() + timedelta(weeks=i))))

        await asyncio.gather(*get_weekly_journals_tasks)

        check_for_test_tasks = []
        async def check_for_test(weekly_journal_model):
            for day in weekly_journal_model:
                for lesson in day.lessons:
                    if lesson.test_scheduled: print(f"ACHTUNG, ALERT, KAPUT!~ {datetime.strftime(day.date, '%d.%m.%y')} - {lesson.title} PĀRBAUDES DARBS, stunda tēma: {lesson.topic}")

    
        for task in get_weekly_journals_tasks:
            check_for_test_tasks.append(asyncio.create_task(check_for_test(task.result())))
        await asyncio.gather(*check_for_test_tasks)


if __name__ == "__main__":
    asyncio.run(main())