class Assignment:
    def __init__(self, name, a_type, score):
        self.name = name
        self.a_type = a_type
        self.score = score
        self.weight = 0

    def weighted_score(self):
        # Weight calculation
        return (self.score * self.weight) / 100 if self.weight > 0 else 0
class GradeCalculator:
    def __init__(self):
        self.assignments = []

    def add_assignment(self, name, a_type, score):
        """Adds an assignment after validating input."""
        if a_type not in ('FA', 'SA'):
            raise ValueError("Type must be 'FA' or 'SA'!")  # validation message
        if not 0 <= score <= 100:
            raise ValueError("Score should be between 0 and 100.")  #  clarifing errors
        self.assignments.append(Assignment(name, a_type, score))

    def calculate_weights(self):
        """Assign weights based on assignment type and relative score."""
        formative = [a for a in self.assignments if a.a_type == 'FA']
        summative = [a for a in self.assignments if a.a_type == 'SA']
        total_fa = sum(a.score for a in formative)
        total_sa = sum(a.score for a in summative)

        # Assigning  weights
        if total_fa > 0:
            for a in formative:
                a.weight = (60 * a.score) / total_fa
        if total_sa > 0:
            for a in summative:
                a.weight = (40 * a.score) / total_sa

    def calculate_totals(self):
        """Calculate totals for Formative and Summative weighted scores."""
        fa_total = sum(a.weighted_score() for a in self.assignments if a.a_type == 'FA')
        sa_total = sum(a.weighted_score() for a in self.assignments if a.a_type == 'SA')
        return fa_total, sa_total

    def check_progression(self):
        """Check if the student can progress based on score thresholds."""
        fa_total, sa_total = self.calculate_totals()
        if fa_total >= 30 and sa_total >= 20:
            return "Congratulations! You passed! :)"
        return "Sorry, you need to retake the assessment. :("

    def resubmission_eligibility(self):
        """List formative assignments below the passing threshold."""
        return [a for a in self.assignments if a.a_type == 'FA' and a.score < 50]

    def display_transcript(self, order='asc'):
        """Print the transcript sorted by score."""
        reverse = order.lower() == 'desc'
        self.assignments.sort(key=lambda x: x.score, reverse=reverse)

        print("\n--- Transcript ---\n")
        print(f"{'Assignment':<15} {'Type':<10} {'Score':<8} {'Weight':<8}")
        for a in self.assignments:
            print(f"{a.name:<15} {a.a_type:<10} {a.score:<8.1f} {a.weight:<8.1f}")


def main():
    print("\n--- Welcome to Course Progress Tracker Application! ---\n")
    calc = GradeCalculator()

    while True:
        name = input("Enter assignment name (or press 'end' to calculate trascript)\n-> : ").strip()
        if name.lower() == 'end':
            break
        try:
            a_type = input("Enter type(FA)Formative/(SA)summative\n-> : ").strip().upper()
            score = float(input("Enter score (0-100)\n-> : "))
            calc.add_assignment(name, a_type, score)
        except ValueError as e:
            print(f"Error:Invalid input, Please try again.")
            continue

    calc.calculate_weights()
    fa_total, sa_total = calc.calculate_totals()

    print("\n--- Results ---\n")
    print(f"Formative Total: {fa_total:.2f}%")
    print(f"Summative Total: {sa_total:.2f}%")
    print(calc.check_progression())

    resubmissions = calc.resubmission_eligibility()
    if resubmissions:
        print("\nAssignments needed to Retake:")
        for a in resubmissions:
            print(f"- {a.name}: {a.score}%")
    else:
        print("\nGreat job! No retakes required.")

    order = input("\nHow would you like the transcript printed? \nAscending order(asc)/ (desc)Descending order: ").strip()
    calc.display_transcript(order)


if __name__ == "__main__":
    main()


