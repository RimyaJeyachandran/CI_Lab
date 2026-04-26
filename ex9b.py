def bayes_spam_filter():

    print("Bayes' Spam Filter")

    try:

        # 1. Get Priors from User

        p_spam = float(input("Enter P(Spam): "))

        p_ham = 1.0 - p_spam

        print(f"set P(Ham) to: {p_ham:.2f}")



        # 2. Get Likelihoods from User

        p_free_given_spam = float(input("Enter P(Free | Spam) : "))

        p_free_given_ham = float(input("Enter P(Free | Ham) : "))



        # 3. Step-by-Step Calculation

        print("\n" + "="*40)

        print("="*40)



        # Numerator: P(Free | Spam) * P(Spam)

        numerator = p_free_given_spam * p_spam

        print(f"P(Free|Spam) * P(Spam)")

        print(f"      {p_free_given_spam} * {p_spam} = {numerator:.4f}")



        # Denominator (Total Probability): P(Free) = P(Free|S)P(S) + P(Free|H)P(H)

        p_free = numerator + (p_free_given_ham * p_ham)

        print(f"\nTotal P(Free)")

        print(f"      ({p_free_given_spam}*{p_spam}) + ({p_free_given_ham}*{p_ham})")

        print(f"      {numerator:.4f} + {p_free_given_ham * p_ham:.4f} = {p_free:.4f}")



        # Final Bayes' Rule Calculation

        p_spam_given_free = numerator / p_free

        print(f"\nP(Spam | Free)")

        print(f"      {numerator:.4f} / {p_free:.4f} = {p_spam_given_free:.4f}")

        print("="*40)



        print(f"\nThe probability the email is spam is {p_spam_given_free:.4f}")



    except ValueError:

        print(" Error: Please enter numerical values (e.g., 0.5).")

    except ZeroDivisionError:

        print("Error: Total probability P(Free) resulted in zero.")



# Run the function

bayes_spam_filter()

