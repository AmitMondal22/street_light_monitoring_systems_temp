def calculate_output(number):
    # Add 1 to the number
    incremented_number = number + 1
    
    # Convert to string
    incremented_str = str(incremented_number)
    
    # Check if there is a decimal part
    if '.' in incremented_str:
        # Split into integer and decimal parts
        integer_part, decimal_part = incremented_str.split('.')
        
        # Count the length of the decimal part
        decimal_length = len(decimal_part)
        
        # Compute the output as 10 raised to the power of the length of the decimal part
        output = 10 ** decimal_length
    else:
        # No decimal part
        output = 1
    
    return output



def dec_to_num(num):
    num2=calculate_output(num)
    hexadecimal_number = hex(num*num2)[2:]
    return hexadecimal_number.upper()
     