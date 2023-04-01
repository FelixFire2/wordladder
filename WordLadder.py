import requests
import logging


def get_filtered_word_list(url):
    response = requests.get(url)
    words = response.text.split('\n')
    filtered_words = [word.strip() for word in words if len(word.strip()) == 4 or len(word.strip()) == 5]
    return filtered_words

def get_filtered_word_list_by_length(url, word_length):
    response = requests.get(url)
    words = response.text.splitlines()
    return [word.strip().lower() for word in words if len(word) == word_length]

def is_one_letter_apart(word1, word2):
    if len(word1) != len(word2):
        return False
    
    difference_count = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            difference_count += 1
            if difference_count > 1:
                return False

    return difference_count == 1

def find_neighbors(word, word_list):
    neighbors = [candidate for candidate in word_list if is_one_letter_apart(word, candidate)]
    return neighbors

def build_ladders(start_word, word_list, ladder_length, logger, word_lists_4, word_lists_5, word_index):
    logger.info(f"TESTING Word {word_index}: {start_word}")
    queue = [(start_word, [start_word])]
    visited = set(start_word)

    while queue:
        current_word, ladder = queue.pop(0)

        if len(ladder) >= 5:
            super_word = build_super_word(ladder)
            match_found = super_word in word_list or any(super_word in wl for _, wl in word_lists_4) or any(super_word in wl for _, wl in word_lists_5)
            log_ladder(logger, ladder, super_word, word_list, word_lists_4, word_lists_5, match_found=match_found)

            if len(ladder) == ladder_length:
                continue

        for neighbor in find_neighbors(current_word, word_list):
            if neighbor not in visited:
                new_ladder = ladder + [neighbor]
                super_word_partial = build_super_word(new_ladder)
                visited.add(neighbor)

                # Check if there are any possible super words with the current prefix
                if any(word.startswith(super_word_partial) for word in word_list):
                    queue.append((neighbor, new_ladder))
                else:
                    log_ladder(logger, new_ladder, None, word_list, word_lists_4, word_lists_5, stopping_path=True)

def setup_logger(log_file_path, log_level="INFO"):
    logger = logging.getLogger("WordLadderLogger")
    logger.setLevel(getattr(logging, log_level))

    # Create file handler and set its log level
    file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
    file_handler.setLevel(getattr(logging, log_level))

    # Create console handler and set its log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger



def build_super_word(ladder):
    super_word = []
    for i in range(1, len(ladder)):
        super_word.append(''.join([a for a, b in zip(ladder[i], ladder[i-1]) if a != b]))
    return ''.join(super_word)

def log_ladder(logger, ladder, super_word, word_list, word_lists_4, word_lists_5, stopping_path=False, match_found=False):
    super_word_partial = build_super_word(ladder)

    if stopping_path:
        stopping_phrase = "Stopping path, no super words possible:"
        logger.debug(f"{stopping_phrase} {' > '.join(ladder)} | {super_word_partial}")
    else:
        if len(ladder) > 1:
            logger.debug(f"{ladder[0]} > {' > '.join(ladder[1:])} | {super_word_partial}")

        if match_found:
            match_phrase = ""
            if super_word in word_list:
                match_phrase = "MATCH!!!"
                additional_info = ""

                if len(super_word) == 4:
                    for name, word_list_4 in word_lists_4:
                        if super_word in word_list_4:
                            additional_info = f" ({name})"
                            break
                    else:
                        additional_info = " (Not in lists)"

                if len(super_word) == 5:
                    for name, word_list_5 in word_lists_5:
                        if super_word in word_list_5:
                            additional_info = f" ({name})"
                            break
                    else:
                        additional_info = " (Not in lists)"

                match_phrase += additional_info

            logger.info(f"{match_phrase} {ladder[0]} > {' > '.join(ladder)} | {super_word}")

    # Flush the log entries
    for handler in logger.handlers:
        handler.flush()


def generate_word_ladders(start_word, word_list, logger, max_ladder_length, word_lists_4, word_lists_5, word_index):
    build_ladders(start_word, word_list, max_ladder_length, logger, word_lists_4, word_lists_5, word_index)

