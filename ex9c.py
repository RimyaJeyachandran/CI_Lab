def weather_analysis_steps():

    print("Weather Probability")



    # R: Rain, C: Cloudy, W: Wet

    combos = [(1,1,1), (1,1,0), (1,0,1), (1,0,0),

              (0,1,1), (0,1,0), (0,0,1), (0,0,0)]



    joint_table = {}

    for r, c, w in combos:

        p = float(input(f"Enter P(Rain={r}, Cloudy={c}, Wet={w}): "))

        joint_table[(r, c, w)] = p



    print("\n" + "="*50)

    print("="*50)



    # 1. Marginal Probability of Rain P(R=1)

    # Get all probabilities where R=1

    rain_probs = [prob for (r, c, w), prob in joint_table.items() if r == 1]

    p_rain = sum(rain_probs)



    print(f"Marginal P(Rain)")

    print(f"Sum of all rows where Rain=1:")

    print(f"P = {' + '.join(map(str, rain_probs))} = {p_rain:.4f}")



    # 2. Conditional Probability P(Rain | Wet)

    # Step A: P(Rain ∩ Wet)

    rw_probs = [prob for (r, c, w), prob in joint_table.items() if r == 1 and w == 1]

    p_rain_and_wet = sum(rw_probs)



    # Step B: P(Wet)

    wet_probs = [prob for (r, c, w), prob in joint_table.items() if w == 1]

    p_wet = sum(wet_probs)



    # Step C: Division

    p_rain_given_wet = p_rain_and_wet / p_wet if p_wet > 0 else 0



    print(f"\nonditional P(Rain | Wet)")

    print(f"Joint P(Rain ∩ Wet): {' + '.join(map(str, rw_probs))} = {p_rain_and_wet:.4f}")

    print(f"Total P(Wet):        {' + '.join(map(str, wet_probs))} = {p_wet:.4f}")

    print(f"P(Rain | Wet) = Joint / Total")

    print(f"   {p_rain_and_wet:.4f} / {p_wet:.4f} = {p_rain_given_wet:.4f}")

    print("="*50)



weather_analysis_steps()

