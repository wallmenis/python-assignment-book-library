import book_authentication as ba

#INITIALIZATION STUFF
auther = ba.Authenticator()

# print("First Line Of Code : )")
auther.start_procedure()
exit_pr = False
while not exit_pr:
    auther.show_menu()
    exit_pr = auther.select_function()
auther.save_all()
