function Mastermindv4()
	clc;   % clear the command window
    % Set up game default parameters
    lengthDigit = 4;
    choiceDigit = 6;
    maxAttempts = 8;
	repeatedDigits ='n';
	name = input('Please enter your name: ', 's');   % Ask the user to enter their name
	% Display a greeting with the entered name
	fprintf('Hello, %s!\n', name);
	disp('Welcome to Text-Based Mastermind!');
    history();
	disp('You are playing Mastermind with 4 unique digits ranging from 1 to 6 and having 8 attempts.')
	disp('Do you want to change the default configuration of the game? (y/n)')
	if YesorNo() =='y'
		% Ask user to choose the game parameters
		fprintf('%s','Please choose the number of digits to guess (4 - 6) : ')
		lengthDigit = user_chosen_config(4,6);
		disp(['Length of digits: ', num2str(lengthDigit)]);
		
		fprintf('%s','Please choose the range of digits to guess, starting from 1 (6 - 9) : ')
		choiceDigit = user_chosen_config(6,9);
		disp(['Range of digits: 1 - ', num2str(choiceDigit)]);
		
		fprintf('%s','Please choose the maximum attempts you want to try (8 - 20) : ')
		maxAttempts = user_chosen_config (8,20);
		disp(['Maximum Attempts: ', num2str(maxAttempts)]);
		
		fprintf('%s','Digits to guess contains repeated digits? (y/n) ')
		repeatedDigits = YesorNo();
		disp(['Digits to guess may contain repeated digits ',repeatedDigits]);
    end	

    % Game loop
	playAgain = true;
	while playAgain
		% Generate a random target digits
		targetDigits = generate_target_Digits(choiceDigit, lengthDigit, repeatedDigits);
		% disp(targetDigits);
		% Initialize variables
		attempts = 0;
		Bingo = false;
		messages = {};
        messageindex = 1;
		messages{messageindex} = '(1:correct position ; 0:correct digit)';
        messageindex = messageindex +1;
		GameStartDateTime = datetime('now');
		% Display game instructions
		% playsound('start.wav');
		disp('Game starts. Enjoy it!');
		disp('----------------------------------------');
		
		while attempts < maxAttempts && ~Bingo
			attempts = attempts + 1;			
			guessDigits = zeros(1, lengthDigit);  % Preallocate an array of size 1xlengthDigit with zeros
			entry_ok = false;
			while ~entry_ok
			    inputMsg = ['Enter ',int2str(lengthDigit),' digits chosen from 1 to ', int2str(choiceDigit), ' without spaces :'];
				userInput = input(inputMsg, 's');
				entry_ok = true;
                % -------------------------------------------
				% First Check: if the number of entered character matches the array size
				if numel(userInput) ~= numel(guessDigits)
					disp('Error: Number of entered digits are not correct.');
					entry_ok = false;
					continue;  % go to while at once
                end
                % End of First Check
                %----------------------------------------
				% Second Check: if entered characters as digit(1,2,3...)
				if ~all(isstrprop(userInput, 'digit'))
					disp('Error: entered characters are not digit.');
					entry_ok = false;
					continue;
                end
                % End of Second Check
                % ---------------------------------------------
                % Third Check: entered digits are within choiceDigit
				for i = 1:numel(guessDigits)
					userInputAsInteger = str2double(userInput(i));
					if userInputAsInteger == 0 || userInputAsInteger > choiceDigit
						disp('Error: entered characters are not within range.');
					    entry_ok = false;
                        break;
					end	
                end
                % End of Third Check
                % --------------------------------------------
            end % while ~entry_ok
            % save to guessDigit when all input are correct
			for i = 1:numel(guessDigits)
				guessDigits(i) = str2double(userInput(i));
			end
			% disp(guessDigits);
			
			% Check guessDigits against targetDigits
			[numCorrectPositions, numCorrectDigits] = checkguessDigits(guessDigits, targetDigits);
			
			% Create the content (finalString) to display for a particulare attempt			
			finalString =['Attempt ' num2str(attempts) '  : '];
			for i=1:lengthDigit
				appendString = num2str(guessDigits(i));
				finalString = [finalString ' '  appendString];
			end
			finalString = [finalString ' | '];
			for i =1:numCorrectPositions
				 finalString = [finalString, ' 1'];
			end

			for i =1:numCorrectDigits
				 finalString = [finalString, ' 0'];
			end
			% Add content in finalString to the message arraty
			messages{messageindex} = finalString;
            messageindex = messageindex +1;
			% clear the screen and print all memorized message again
            clc;
            for i = 1: (messageindex-1)
                disp(char(messages(i)));  % show message without the bracket
			end
            disp(' ');
			
			% Check if the game is won
			if numCorrectPositions == lengthDigit
				Bingo = true;
			end
        end 
    
		% Game result
		% playsound('bingo.wav');
		if Bingo
			disp('Congratulations! You find the target digits.');
		else
			disp('Sorry, you cannot find the target digits within allowed attempts.');
			disp(['The target digits are: ', num2str(targetDigits)]);
		end
		disp('Do you want to save the game result? (y/n): ')  % Ask if the user wants to save the game result
		if YesorNo() =='y'
			saveRecord(name, lengthDigit, choiceDigit, repeatedDigits, GameStartDateTime, attempts, Bingo);
		end
        disp('Do you want to play again? (y/n): ')  		% Ask if the user wants to play again
		if YesorNo() =='n'   % Check the user's choice
			playAgain = false;
			disp('Thank you for playing!');
        end 
    end % while attempts < maxAttempts && ~Bingo	
end   % while playAgain



function targetDigits = generate_target_Digits(choiceDigit, lengthDigit, includeRepeatDigit)
    % Generate random target digits
    targetDigits = randperm(choiceDigit, lengthDigit);   	% unique digits
	if includeRepeatDigit=='y'
		% with repeated digit
		switch lengthDigit
			case 4
				digitRepeats =[4 4 4 4];
			case 5
				digitRepeats =[5 5 5 5 5];
			case 6
				digitRepeats =[6 6 6 6 6 6];
		end
		% 1st digit x 1, 2nd digit x 2, 3rd digit x 3, 4th digit x 4, 5th digit x 5, 6th digit x 6
		repeatedElements = repelem(targetDigits, digitRepeats); 
		% randperm(numel(sequence)) generates a random permutation of the indices of the  sequence array. 
		% The numel(sequence) returns the total number of elements in the sequence array.
		% The resulting randperm permutation is then used to index the sequence array, effectively shuffling the elements randomly.
		shuffledSequence = repeatedElements(randperm(numel(repeatedElements)));
		% elects the elements from index 1 to index (lengthDigit) of the longArray array shuffledSequence
		targetDigits = shuffledSequence(1:lengthDigit);
	end	
end

function [num_CorrectPositions, num_CorrectDigits] = checkguessDigits(guessDigits, targetDigits)
	num_CorrectPositions = 0;
	for i = 1:length(guessDigits)
		if (guessDigits(i) == targetDigits(i))
			guessDigits(i)=0;
			targetDigits(i)=0;
			num_CorrectPositions = num_CorrectPositions + 1;
		end
	end 
	
	num_CorrectDigits = 0;
	for i = 1:length(guessDigits)
		for j = 1:length(targetDigits)
			if (guessDigits(i) ~=0 && targetDigits(j) ~=0)
				if (guessDigits(i) == targetDigits(j))
					num_CorrectDigits = num_CorrectDigits + 1;
					guessDigits(i)=0;
					targetDigits(j)=0;
				end
			end
		end		
	end
end

% Following function restrict the user to only input valid value
function userInput = user_chosen_config(minValue, maxValue) 
    pass_all= false;
    while ~pass_all
        userInput = input('','s' );
        if all(isstrprop(userInput, 'digit'))
            pass_all=true;
            userInput = str2double(userInput);  
            if (userInput < minValue || userInput > maxValue)
                pass_all=false;
                fprintf("Input not within specified range.\nPlease enter integers within the specified range: " );
            end
        else 
            fprintf("Input is not a digit.\nPlease enter integers within the specified range: ");
        end 
    end
end

% Following function restrict the user either enter Y,y,N,n
function userInput = YesorNo()
	validResponses = {'y', 'n'}; 
    userInput = input('', 's'); % input string
	userInput = lower(userInput);
    while ~ismember(userInput, validResponses)
        userInput = input('Invalid input. Please enter either "y" or "n": ', 's');
		userInput = lower(userInput);
    end
end

function saveRecord(name, numDigit, rangeDigit, repeatDigit, GameStartDateTime, attempts, WinLoss)
	% Get the current date and time
	currentDateTime = datetime('now');
	fileID = fopen('MM_record.txt', 'a');   % Open the text file in append mode
	% Write the user information to the file
	fprintf(fileID, 'Name: %s\n', name);
	fprintf(fileID, 'Number of Digits to guess: %s\n', num2str(numDigit));
	fprintf(fileID, 'Range of Digits to guess: %s\n', num2str(rangeDigit));
	if repeatDigit == 'y'
		fprintf(fileID, 'Any repeated digit to guess: %s\n', 'Yes');
	else
		fprintf(fileID, 'Any repeated digit to guess: %s\n', 'No');
	end
	fprintf(fileID, 'Attempts: %d\n', attempts);
	if WinLoss
		fprintf(fileID, 'Result: %s\n', 'Win');
        
	else
		fprintf(fileID, 'Result: %s\n', 'Loss');
	end
	fprintf(fileID, 'Game start time: %s\n', string(GameStartDateTime));
	minutesElapsed = minutes(currentDateTime - GameStartDateTime);
	fprintf(fileID, 'Time spent for this round (minutes): %s\n', num2str(minutesElapsed));
	fprintf(fileID, '----------\n');	
	fclose(fileID);   % Close the file
	% Display a confirmation message
	fprintf('User record has been saved to "MM_record.txt".\n');
end

function playsound(filePath)
	% Read the WAV file
	[soundData, fs] = audioread(filePath);
	% Play the sound
	sound(soundData, fs);
end

function history()
    disp(' ');
	% Open the file for reading
	fileID = fopen('MM_record.txt', 'r');
	if fileID == -1    % File could not be opened
		return;
	else
        filecontent = fscanf(fileID, '%c');   % Read the data from the file
        fclose(fileID);  % Close the file
        %count the number of lines
        numLines = numel(strfind(filecontent,newline));
        if numLines >= 9
            disp("The record of the last player: ")
            lines = splitlines(filecontent);
            % Calculate the starting line index
            startLineIndex = numLines - 9 + 1;
	        % Display the lines
	        for i = startLineIndex:numLines
		        disp(lines{i});
	        end
        end   
    end   
end
