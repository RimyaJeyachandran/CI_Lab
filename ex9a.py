def vending_machine_prob():

    print("Vending Machine Inventory Probability")

    try:

        # 1. Get Inventory Details from User

        total_items = int(input("Enter total items in machine: "))

        expired = int(input("Enter number of expired items: "))

        fresh = total_items - expired



        print(f" Calculated Fresh items: {fresh}")



        # 2. Logic: The 'available pool' (excluding the current item being viewed)

        available_pool = total_items - 1



        if available_pool <= 0:

            print("Error: Not enough items in the machine to calculate probability.")

            return None



        # 3. Calculation

        prob_expired = expired / available_pool



        # 4. Display Steps

        print("\n" + "="*40)

        print("="*40)

        print(f"Total Items:      {total_items}")

        print(f"Expired Items:    {expired}")

        print(f"Available Pool:   {total_items} - 1 = {available_pool}")

        print(f"Calculation:      {expired} / {available_pool}")

        print("="*40)



        return prob_expired



    except ValueError:

        print("Error: Please enter whole numbers for inventory items.")

        return None



# Run and Print Result

result = vending_machine_prob()

if result is not None:

    print(f"\nProb of Next is Expired: {result:.4f}")

