from habit_service.service import HabitService
from habit_storage.json_storage import HabitJsonStorage
from schemas.habit_schema import (
    CategoryHabit,
    DailyHabitSchema,
    WeeklyHabitSchema,
    TypeHabit,
)


def menu():
    print("=" * 10, "MENU", "=" * 10)
    print("1. Create Habit")
    print("2. Delete Habits")
    print("3. Complete Habit")
    print("4. Show Habit")
    print("5. Show All Habits")
    print("6. Show Achievement")
    print("7. Show all achievements")
    print("8. Exit")
    print("=" * 10, "MENU", "=" * 10)


def create_habit_menu():
    print("=" * 10, "CREATE HABIT", "=" * 10)
    print("1. Daily Habit")
    print("2. Weekly Habit")
    print("3. Exit to main menu")
    print("=" * 10, "CREATE HABIT", "=" * 10)


def category_menu():
    print("=" * 10, "CATEGORY", "=" * 10)
    print("1. Health")
    print("2. Productivity")
    print("3. Sports")
    print("4. Self Development")
    print("5. Finance")
    print("6. Other")
    print("7. Exit to main menu")
    print("=" * 10, "CATEGORY", "=" * 10)


def delete_habits_menu():
    print("=" * 10, "DELETE HABIT", "=" * 10)
    print("1. Delete Habit")
    print("2. Delete All Habits")
    print("3. Exit to main menu")
    print("=" * 10, "DELETE HABIT", "=" * 10)


def delete_all_habits_menu():
    print("=" * 10, "Do you want to delete the habit?", "=" * 10)
    print("1. Yes")
    print("2. No")
    print("=" * 54)


def show_habit_menu():
    habit_service = HabitService(HabitJsonStorage())

    while True:
        menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                create_habit_menu()

                choice = input("Enter your choice: ")

                if choice == "1":
                    habit_name = input("Enter your habit name: ").strip()
                    habit_description = input("Enter your habit description: ").strip()

                    while True:
                        category_menu()

                        category = input("Select a habit category: ")
                        if category == "1":
                            category = CategoryHabit.HEALTH
                        elif category == "2":
                            category = CategoryHabit.PRODUCTIVITY
                        elif category == "3":
                            category = CategoryHabit.SPORTS
                        elif category == "4":
                            category = CategoryHabit.SELF_DEVELOPMENT
                        elif category == "5":
                            category = CategoryHabit.FINANCE
                        elif category == "6":
                            category = CategoryHabit.OTHER
                        elif category == "7":
                            print("Exiting to main menu...")
                            break
                        else:
                            print("Invalid category selected")
                            continue

                        print(
                            habit_service.create_habit(
                                type_habit=TypeHabit.DAILY,
                                daily_schema=DailyHabitSchema(
                                    habit_name=habit_name,
                                    habit_description=habit_description,
                                    category=category,
                                ),
                            )
                        )
                        break
                    break

                elif choice == "2":
                    habit_name = input("Enter your habit name: ").strip()
                    habit_description = input("Enter your habit description: ").strip()

                    while True:
                        category_menu()

                        category = input("Select a habit category: ")
                        if category == "1":
                            category = CategoryHabit.HEALTH
                        elif category == "2":
                            category = CategoryHabit.PRODUCTIVITY
                        elif category == "3":
                            category = CategoryHabit.SPORTS
                        elif category == "4":
                            category = CategoryHabit.SELF_DEVELOPMENT
                        elif category == "5":
                            category = CategoryHabit.FINANCE
                        elif category == "6":
                            category = CategoryHabit.OTHER
                        elif category == "7":
                            print("Exiting to main menu...")
                            break
                        else:
                            print("Invalid category selected")
                            continue

                        print(
                            habit_service.create_weekly_habit(
                                type_habit=TypeHabit.WEEKLY,
                                weekly_schema=WeeklyHabitSchema(
                                    habit_name=habit_name,
                                    habit_description=habit_description,
                                    category=category,
                                ),
                            )
                        )
                        break
                    break

                elif choice == "3":
                    print("Exiting to main menu...")
                    break

                else:
                    print("Invalid choice")
                    continue

        elif choice == "2":
            while True:
                delete_habits_menu()
                choice = input("Enter your choice: ")

                if choice == "1":
                    habit_id = int(input("Enter your habit id for delete: "))
                    print(habit_service.delete_habit(habit_id))

                elif choice == "2":
                    delete_all_habits_menu()
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        print(habit_service.delete_all_habits())
                        break
                    elif choice == "2":
                        print("Exiting to main menu...")
                        break
                    else:
                        print("Invalid choice")  # ??????
                elif choice == "3":
                    print("Exiting to main menu...")
                    break
                else:
                    print("Invalid choice")
                continue

        elif choice == "3":
            habit_id = int(input("Enter the habit id to perform: "))
            print(habit_service.complete_habit(habit_id))

        elif choice == "4":
            habit_id = int(input("Enter the habit id to show: "))
            print(habit_service.show_habit(habit_id))

        elif choice == "5":
            print(habit_service.show_all_habits())

        elif choice == "6":
            habit_id = int(input("Enter the habit id: "))
            print(habit_service.show_achievement(habit_id))

        elif choice == "7":
            print(habit_service.show_all_achievements())

        elif choice == "8":
            exit("Thank you for using this program!")

        else:
            print("Invalid choice")
            continue


if __name__ == "__main__":
    show_habit_menu()
