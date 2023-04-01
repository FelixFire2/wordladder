import requests
from WordLadder import get_filtered_word_list, generate_word_ladders, setup_logger, get_filtered_word_list_by_length

word_list_url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
log_file_path = "E:/Python/WordLadder.log"
max_ladder_length = 6

word_list_4_urls = ["https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"]  # Replace with actual URLs
word_list_5_urls = ["https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"]  # Replace with actual URLs

def process_combinations(word_list, log_file_path, max_ladder_length, word_lists_4, word_lists_5):
    logger = setup_logger(log_file_path, "INFO")
    logger.info(f"Number of words in the filtered word list: {len(word_list)}")

    for index, start_word in enumerate(word_list):
        generate_word_ladders(start_word, word_list, logger, max_ladder_length, word_lists_4, word_lists_5, word_index=index + 1)

if __name__ == "__main__":
    word_list = get_filtered_word_list(word_list_url)
    word_lists_4 = [(f"List 4-{i+1}", get_filtered_word_list_by_length(url, 4)) for i, url in enumerate(word_list_4_urls)]
    word_lists_5 = [(f"List 5-{i+1}", get_filtered_word_list_by_length(url, 5)) for i, url in enumerate(word_list_5_urls)]

    process_combinations(word_list, log_file_path, max_ladder_length, word_lists_4, word_lists_5)
