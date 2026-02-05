from habit_service.service import HabitService
from habit_storage.json_storage import HabitJsonStorage
from schemas.habit_schema import (
    CategoryHabit,
    DailyHabitSchema,
    WeeklyHabitSchema,
    TypeHabit,
)


class HabitTrackerCLI:
    def __init__(self):
        self.habit_service = HabitService(HabitJsonStorage())

    def main_menu(self):
        print("=" * 10, "MENU", "=" * 10)
        print("1. Create Habit")
        print("2. Delete Habits")
        print("3. Complete Habit")
        print("4. View Habits")
        print("5. View Achievement")
        print("6. Exit")
        print("=" * 10, "MENU", "=" * 10)

        choice = input("Enter your choice: ")

        if choice == "1":
            self._create_habit_menu()
        elif choice == "2":
            self._delete_habits_menu()
        elif choice == "3":
            habit_id = int(input("Enter the habit id to perform: "))
            print(self.habit_service.complete_habit(habit_id))
            self.main_menu()
            return
        elif choice == "4":
            self._view_habits()
        elif choice == "5":
            self._view_achievements()
        elif choice == "6":
            exit("Thank you for using this program!")

    def _create_habit_menu(self):
        print("=" * 10, "CREATE HABIT", "=" * 10)
        print("1. Daily Habit")
        print("2. Weekly Habit")
        print("3. Back")
        print("=" * 10, "CREATE HABIT", "=" * 10)

        choice = int(input("Enter your choice: "))

        if choice == 3:
            self.main_menu()
            return

        if choice not in [1, 2]:
            print("Invalid choice. Please select 1, 2, or 3.")
            self._create_habit_menu()
            return

        habit_name = input("Enter your habit name: ").strip()
        habit_description = input("Enter your habit description: ").strip()

        type_habit_map = {
            1: TypeHabit.DAILY,
            2: TypeHabit.WEEKLY,
        }
        type_habit = type_habit_map[choice]

        if self._category_menu(habit_name, habit_description, type_habit):
            return

    def _category_menu(self, habit_name, habit_description, type_habit):
        print("=" * 10, "CATEGORY", "=" * 10)
        print("1. Health")
        print("2. Productivity")
        print("3. Sports")
        print("4. Self Development")
        print("5. Finance")
        print("6. Other")
        print("7. Exit to main menu")
        print("=" * 10, "CATEGORY", "=" * 10)

        category_map = {
            1: CategoryHabit.HEALTH,
            2: CategoryHabit.PRODUCTIVITY,
            3: CategoryHabit.SPORTS,
            4: CategoryHabit.SELF_DEVELOPMENT,
            5: CategoryHabit.FINANCE,
            6: CategoryHabit.OTHER,
        }

        choice = int(input("Select a habit category: "))

        if choice == 7:
            self.main_menu()

        if choice not in category_map:
            print("Invalid choice. Please select a number between 1 and 7.")

        category = category_map[choice]
        try:
            if type_habit == TypeHabit.DAILY:
                print(
                    self.habit_service.create_habit(
                        type_habit=TypeHabit.DAILY,
                        daily_schema=DailyHabitSchema(
                            habit_name=habit_name,
                            habit_description=habit_description,
                            category=category,
                        ),
                    )
                )
                self.main_menu()
                return
            elif type_habit == TypeHabit.WEEKLY:
                print(
                    self.habit_service.create_weekly_habit(
                        type_habit=TypeHabit.WEEKLY,
                        weekly_schema=WeeklyHabitSchema(
                            habit_name=habit_name,
                            habit_description=habit_description,
                            category=category,
                        ),
                    )
                )
                self.main_menu()
                return
        except ValidationError as e:
            print(f"Data validation error: {e}")
            self._create_habit_menu()
            return

    def _delete_habits_menu(self):
        print("=" * 10, "DELETE HABIT", "=" * 10)
        print("1. Delete Habit by ID")
        print("2. Delete All Habits")
        print("3. Back")
        print("=" * 10, "DELETE HABIT", "=" * 10)

        choice = input("Enter your choice: ")

        if choice == "1":
            habit_id = int(input("Enter your habit id for delete: "))
            print(self.habit_service.delete_habit(habit_id))
            self._delete_habits_menu()
            return

        elif choice == "2":
            self._delete_all_habits_menu()

        elif choice == "3":
            self.main_menu()
            return

    def _delete_all_habits_menu(self):
        print("=" * 10, "Do you want to delete the habit?", "=" * 10)
        print("1. Yes")
        print("2. No")
        print("=" * 54)

        choice = input("Enter your choice: ")

        if choice == "1":
            print(self.habit_service.delete_all_habits())
            self.main_menu()
            return

        elif choice == "2":
            self._delete_habits_menu()
            return

    def _view_habits(self):
        print("=" * 10, "View Habits", "=" * 10)
        print("1. Show Habit by ID")
        print("2. Show All Habits")
        print("3. Back")
        print("=" * 10, "View Habits", "=" * 10)

        choice = input("Enter your choice: ")

        if choice == "1":
            habit_id = int(input("Enter your habit id for view: "))
            print(self.habit_service.show_habit(habit_id))
            self._view_habits()
            return

        elif choice == "2":
            print(self.habit_service.show_all_habits())
            self._view_habits()
            return

        elif choice == "3":
            self.main_menu()
            return

    def _view_achievements(self):
        print("=" * 10, "View Achievements", "=" * 10)
        print("1. Show Achievement by ID")
        print("2. Show All Achievements")
        print("3. Back")
        print("=" * 10, "View Achievements", "=" * 10)

        choice = input("Enter your choice: ")

        if choice == "1":
            habit_id = int(input("Enter the habit id: "))
            print(self.habit_service.show_achievement(habit_id))
            self._view_achievements()
            return

        elif choice == "2":
            print(self.habit_service.show_all_achievements())
            self._view_achievements()
            return

        elif choice == "3":
            self.main_menu()
            return


if __name__ == "__main__":
    cli = HabitTrackerCLI()
    cli.main_menu()
