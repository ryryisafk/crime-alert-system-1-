
def generate_reasoning(row, prediction, averages):

    reasoning = []
    recommendations = []

    # Reasoning
    if row["crime_rate"] > averages["crime_rate"]:
        reasoning.append("Crime rate exceeds the state average.")

    if row["pendency_rate"] > averages["pendency"]:
        reasoning.append("Case pendency exceeds the state average.")

    if row["conviction_rate"] < averages["conviction"]:
        reasoning.append("Conviction rate is below the state average.")

    if row["crime_count"] > averages["crime_count"]:
        reasoning.append("Reported crime volume is higher than the state average.")

    # Make sure at least one reason is always present
    if len(reasoning) == 0:
        if prediction == "High":
            reasoning.append(
                "The machine learning model identified a high-risk pattern based on the combination of crime indicators."
            )

        elif prediction == "Medium":
            reasoning.append(
                "Several indicators together suggest a moderate level of crime risk."
            )

        else:
            reasoning.append(
                "Current crime indicators remain within expected levels."
            )

    # Recommendations
    if prediction == "High":

        recommendations.append("Increase patrol frequency.")
        recommendations.append("Conduct public awareness campaigns.")
        recommendations.append("Monitor repeat offenders.")

    elif prediction == "Medium":

        recommendations.append("Increase surveillance in vulnerable areas.")
        recommendations.append("Review recent crime trends regularly.")
        recommendations.append("Coordinate with local police units.")

    else:

        recommendations.append("Maintain routine monitoring.")
        recommendations.append("Continue preventive policing.")
        recommendations.append("Promote community awareness initiatives.")

    return {
        "reasoning": reasoning,
        "recommendations": recommendations
    }