
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1].resolve()))

from kivy.clock import Clock
from morphui.app import MorphApp
from morphui.uix.dataview import MorphDataViewTable

class MyApp(MorphApp):
    def build(self) -> MorphDataViewTable:
        self.theme_manager.theme_mode = 'Dark'
        self.theme_manager.seed_color = 'morphui_teal'

        self.table = MorphDataViewTable(
            rows_per_page=53,)

        Clock.schedule_once(self.set_data, 0)
        return self.table

    def set_data(self, *args) -> None:
        self.table.column_names = [
            'Name', 'Age', 'Occupation', 'Country', 'Email', 'Phone', 'Company',
            'Position', 'Department', 'Start Date', 'End Date', 'Status',
            'Notes', 'Salary', 'Bonus', 'Manager', 'Team', 'Location',
            'Project', 'Task', 'Deadline', 'Priority', 'Comments', 'Feedback',
            'Rating', 'Score', 'Level', 'Experience', 'Skills', 'Certifications',
            'Languages', 'Hobbies', 'Interests', 'Social Media', 'Website',]
        self.table.values = [[
            f'Name {i}',
            str(20 + i % 30),
            'Occupation ' + str(i % 10),
            'Country ' + str(i % 5),
            'email' + str(i) + '@example.com',
            '123-456-7890',
            'Company ' + str(i % 7),
            'Position ' + str(i % 8),
            'Department ' + str(i % 6),
            '2020-01-01',
            '2023-12-31',
            'Active' if i % 2 == 0 else 'Inactive',
            'Notes for entry ' + str(i),
            str(50000 + (i % 10) * 5000),
            str(5000 + (i % 5) * 1000),
            'Manager ' + str(i % 4),
            'Team ' + str(i % 3),
            'Location ' + str(i % 6),
            'Project ' + str(i % 9),
            'Task ' + str(i % 12),
            '2023-12-' + str(10 + i % 20).zfill(2),
            'High' if i % 3 == 0 else 'Low',
            'Comments for entry ' + str(i),
            'Feedback for entry ' + str(i),
            str(1 + i % 5),
            str(50 + i % 50),
            str(1 + i % 4),
            str(1 + i % 10) + ' years',
            'Skill ' + str(i % 15),
            'Certification ' + str(i % 7),
            'Language ' + str(i % 5),
            'Hobby ' + str(i % 8),
            'Interest ' + str(i % 6),
            'http://socialmedia' + str(i) + '.com',
            'http://website' + str(i) + '.com',
            ]
            for i in range(1, 51)]
        self.table.row_names = [f'Row {i}' for i in range(1, 51)]

if __name__ == "__main__":
    MyApp().run()