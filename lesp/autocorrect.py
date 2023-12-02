"""
LESP helps you to detect and correct spelling mistakes in your text. It is a Python library that uses the Levenshtein distance algorithm to find similar words in a wordlist. Overall it works quickly and does not require a lot of resources.
"""
from typing import List, Optional, Union
import concurrent.futures
import os
import json

class Proofreader:
    """
    Proofreader - The main component of LESP. Contains most of the functions and methods of the library.

    Args:
        wordlist_path (str): Path to the wordlist file. Defaults to "lesp-wordlist.txt".
        cache_file (str): Path to the cache file. Defaults to "lesp_cache/lesp.cache".
    
    Attributes:
        wordlist_path (str): Path to the wordlist file.
        wordlist (List[str]): List of words in the wordlist.
        cache_file (str): Path to the cache file.
        cache (dict): Dictionary containing the cache data.
    
    Raises:
        FileNotFoundError: If the wordlist file or cache file is not found.
        ValueError: If the wordlist file is not in the correct format.
        ValueError: If the cache file is not in the correct format.
        json.JSONDecodeError: If the cache file is not a valid JSON file.
    
    Methods:
        load_wordlist: Loads the wordlist file.
        load_cache: Loads the cache file.
        save_cache: Saves the cache file.
        get_similarity_score: Calculates the similarity score between two words.
        get_similar: Returns a list of similar words.
        is_correct: Checks if a word is correct.
        backup: Backs up the wordlist file.
        restore: Restores the wordlist file from a backup.
        extend_wordlist: Adds a word or a list of words to the wordlist.
        remove_from_wordlist: Removes a word or a list of words from the wordlist.
        stack: Stacks two wordlist files.
        merge_delete: Merges two wordlist files and deletes the words in the first file from the second file.
        clear_cache: Clears the cache file.
    """
    def __init__(self, wordlist_path: str = "lesp-wordlist.txt", cache_file: str = "lesp_cache/lesp.cache") -> None:
        self.wordlist_path: str = wordlist_path
        self.load_wordlist()
        self.cache_file: str = cache_file
        self.cache: dict = {}
        self.wordlist: List[str] = []
        if cache_file:
            self.load_cache(cache_file)

    def load_wordlist(self) -> None:
        """
        Loads a wordlist, also can be used to dynamically switch between wordlists. The wordlist path is based on the wordlist_path attribute of the Proofreader object.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            FileNotFoundError: If the wordlist file is not found.
            ValueError: If the wordlist file is not in the correct format.
        
        Requires:
            The wordlist file must be in the correct format. Each word must be on a separate line. Words must contain only alphabetic characters.
        """
        try:
            with open(self.wordlist_path, "r") as f:
                self.wordlist: List[str] = f.read().strip().split("\n")
                # Remove duplicate words in the wordlist
                self.wordlist = list(set(self.wordlist))
                # Remove leading and trailing whitespaces from each word
                self.wordlist = [word.strip() for word in self.wordlist]
            if not all(word.isalpha() for word in self.wordlist):
                raise ValueError("Invalid wordlist format. Words must contain only alphabetic characters.")
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.wordlist_path} not found!")
    
    def load_cache(self, cache_file: str = "lesp.cache") -> None:
        """
        Loads the cache file. The cache file path is provided to the method as an argument.

        Args:
            cache_file (str): Path to the cache file.
        
        Returns:
            None
        
        Raises:
            FileNotFoundError: If the cache file is not found.
            ValueError: If the cache file is not in the correct format.
            json.JSONDecodeError: If the cache file is not a valid JSON file.
        """
        try:
            with open(cache_file, "r") as f:
                # Validate cache file format and how words are stored
                temp_cache: dict = json.load(f)
                # Must follow the format {"word": ["similar", "words"]}
                if not all(isinstance(word, str) for word in temp_cache.keys() and not all(word.islower() and word.isalpha() for word in temp_cache.keys())):
                    raise ValueError("Invalid cache file format. Keys must be strings. Also the strings must be all-lowercase and contain only alphabetic characters.")
                self.cache: dict = json.load(f)
        except FileNotFoundError:
            # Create the cache file (and directory. also possible if multiple directories are missing)
            try:
                os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                with open(cache_file, "w") as f:
                    json.dump({}, f)
            except:
                with open(cache_file, "w") as f:
                    json.dump({}, f)
        except json.JSONDecodeError:
            raise ValueError("Invalid cache file format. Must be a valid JSON file.")
        
    def save_cache(self) -> None:
        """
        Saves the cache file. The cache file path is specified in the Proofreader object.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            FileNotFoundError: If the cache file is not found.
        """
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self.cache, f)
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.cache_file} not found!")

    @staticmethod
    def get_similarity_score(word1: str, word2: str) -> float:
        """
        Calculates the similarity score between two words using the Levenshtein distance algorithm.

        Args:
            word1 (str): First word.
            word2 (str): Second word.
        
        Returns:
            float: Similarity score between the two words.
        
        Raises:
            None
        
        Requires:
            The two words must be strings.
        """
        len1: int = len(word1)
        len2: int = len(word2)
        matrix: List[List[int]] = [[0 for j in range(len2 + 1)] for i in range(len1 + 1)]

        for i in range(len1 + 1):
            matrix[i][0] = i
        for j in range(len2 + 1):
            matrix[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost: int = 0 if word1[i - 1] == word2[j - 1] else 1
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)

        score: float = 1 - matrix[len1][len2] / max(len1, len2)
        return score

    @staticmethod
    def get_similar_worker(args: tuple) -> List[str]:
        """
        WARNING: DO NOT USE THIS METHOD DIRECTLY. USE THE get_similar METHOD INSTEAD.

        Args:
            args (tuple): Tuple containing the word, similarity rate, and the wordlist chunk.
        
        Returns:
            List[str]: List of similar words.
        
        Raises:
            None
        
        Requires:
            The word must be a string.
            The similarity rate must be a float between 0 and 1.
            The wordlist chunk must be a list of strings.
        """
        word: str
        similarity_rate: float
        wordlist_chunk: List[str]
        word, similarity_rate, wordlist_chunk = args
        similar_words: List[str] = []
        for w in wordlist_chunk:
            score: float = Proofreader.get_similarity_score(word, w)
            if score >= similarity_rate:
                similar_words.append(w)
        return similar_words

    def is_correct(self, word: str) -> bool:
        """
        Checks if a word is correct.

        Args:
            word (str): Word to check.
        
        Returns:
            bool: True if the word is correct, False otherwise.
        
        Raises:
            None
        
        Requires:
            The word must be a string.
        """
        return word.lower() in self.wordlist

    def get_similar(self, word: str, similarity_rate: float, chunks: int = 4, upto: int = 3, use_cache: bool = False, set_cache: bool = False):
        """
        Returns a list of similar words, if any. If no similar words are found, returns None.

        Args:
            word (str): Word to check.
            similarity_rate (float): Similarity rate between 0 and 1.
            chunks (int): Number of chunks to split the wordlist into. Defaults to 4.
            upto (int): Number of similar words to return. Defaults to 3.
            use_cache (bool): Whether to use the cache file. Defaults to False.
            set_cache (bool): Whether to set the cache file. Defaults to False.
        
        Returns:
            List[str]: List of similar words.
            or None if no similar words are found.
        
        Raises:
            ValueError: If upto is less than 1.
            ValueError: If chunks is less than 1.
            ValueError: If similarity_rate is not between 0 and 1.
        
        Requires:
            The word must be a string.
            The similarity rate must be a float between 0 and 1.
            The wordlist chunk must be a list of strings.
        """
        if upto < 1:
            raise ValueError("Can only return 1 or more similar words.")
        if chunks < 1:
            raise ValueError("Can only split into 1 or more chunks.")
        if similarity_rate < 0 or similarity_rate > 1:
            raise ValueError("Similarity rate must be between 0 and 1.")

        word = word.lower()
        similar_words: List[str] = []
        chunk_size: int = len(self.wordlist) // chunks

        if use_cache and self.cache and self.cache_file and word in self.cache:
            if self.cache[word] != []:
                return self.cache[word][:upto]
            else:
                return None

        chunks: List[tuple] = [(word, similarity_rate, self.wordlist[i:i + chunk_size]) for i in range(0, len(self.wordlist), chunk_size)]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results: List[List[str]] = list(executor.map(Proofreader.get_similar_worker, chunks))

        for similar_word_list in results:
            similar_words.extend(similar_word_list)

        similar_words = list(set(similar_words))

        if set_cache and self.cache_file and word not in self.cache:
            print("Setting cache for \"" + word + "\"")
            self.cache[word] = similar_words
            self.save_cache()


        if len(similar_words) == 0:
            return None
        else:
            # Return only upto similar words
            return similar_words[:upto]

    def backup(self, path: str = "wordlist_backup") -> None:
        """
        Backs up the wordlist file.

        Args:
            path (str): Path to the backup file.
        
        Returns:
            None
        
        Raises:
            ValueError: If the path specified is a directory.
        """
        if os.path.isdir(path):
            raise ValueError("Path specified is a directory!")
        with open(path, "w") as f:
            f.write("\n".join(self.wordlist))

    def restore(self, overwrite_current: bool, path: str = "wordlist_backup") -> None:
        """
        Restores the wordlist file from a backup.

        Args:
            overwrite_current (bool): Whether to overwrite the current wordlist file.
            path (str): Path to the backup file.
        
        Returns:
            None

        Raises:
            FileNotFoundError: If the backup file is not found.
            ValueError: If the backup file is not in the correct format.
        
        Requires:
            The backup file must be in the correct format. Each word must be on a separate line. Words must contain only alphabetic characters.
        """
        try:
            if not os.path.isfile(path):
                raise FileNotFoundError("Backup file not found!")

            with open(path, "r") as f:
                wordlist_: List[str] = f.read().split("\n")

            if not all(word.isalpha() for word in wordlist_):
                raise ValueError("Invalid backup file format. Words must contain only alphabetic characters.")
        
            # Same validation as load_wordlist but optimized for this method
            wordlist_ = list(set(wordlist_))

            # Remove leading and trailing whitespaces from each word
            wordlist_ = [word.strip() for word in wordlist_]

            if not all(word.isalpha() for word in wordlist_ and not all(word.islower() for word in wordlist_)):
                raise ValueError("Invalid backup file format. Words must be all-lowercase and contain only alphabetic characters.")

            self.wordlist = wordlist_

            if overwrite_current:
                with open(self.wordlist_path, "w") as f:
                    f.write("\n".join(self.wordlist))
        except Exception as e:
            raise ValueError(f"Error during restore: {str(e)}")

    def extend_wordlist(self, word: Union[str, List[str], tuple]) -> None:
        """
        Adds a word or a list of words to the wordlist.

        Args:
            word (Union[str, List[str], tuple]): Word or list of words to add to the wordlist.
        
        Returns:
            None
        
        Raises:
            TypeError: If the input type is not a string, list, or tuple.
            ValueError: If the input is not a valid word.
        
        Requires:
            Each word must be a string.
            Each word must be alphabetic.
        """
        if isinstance(word, str):
            if word.isalpha():
                self.wordlist.append(word.lower())
            else:
                raise ValueError(f"Invalid input: '{word}' is not a valid word.")
        elif isinstance(word, (list, tuple)):
            for w in word:
                if isinstance(w, str) and w.isalpha():
                    self.wordlist.append(w.lower())
                else:
                    raise ValueError(f"Invalid input: '{word}' is not a valid word.")
        else:
            raise TypeError("Invalid input type. Please provide a string, list, or tuple of alphabetic words.")

    def remove_from_wordlist(self, word: Union[str, List[str], tuple]) -> None:
        """
        Removes a word or a list of words from the wordlist.

        Args:
            word (Union[str, List[str], tuple]): Word or list of words to remove from the wordlist.
        
        Returns:
            None
        
        Raises:
            TypeError: If the input type is not a string, list, or tuple.
            ValueError: If the input is not a valid word.
        
        Requires:
            Each word must be a string.
            Each word must be alphabetic.
        """
        if isinstance(word, str):
            if word.isalpha():
                if word in self.wordlist:
                    self.wordlist.remove(word)
                else:
                    raise ValueError(f"\"{word}\" not in wordlist!")
            else:
                raise ValueError(f"Invalid input: '{word}' is not a valid word.")
        elif isinstance(word, (list, tuple)):
            for w in word:
                if isinstance(w, str) and w.isalpha():
                    if w in self.wordlist:
                        self.wordlist.remove(w)
                    else:
                        raise ValueError(f"\"{w}\" not in wordlist!")
                else:
                    raise ValueError(f"Invalid input: '{word}' is not a valid word.")
        else:
            raise TypeError("Invalid input type. Please provide a string, list, or tuple of alphabetic words.")

    @staticmethod
    def stack(source: str, destination: str) -> None:
        """
        Stacks two wordlist files. The source file is stacked on top of the destination file.

        Args:
            source (str): Path to the source file.
            destination (str): Path to the destination file.
        
        Returns:
            None
        
        Raises:
            FileNotFoundError: If the source file or destination file is not found.
            ValueError: If the source file is not in the correct format.
            ValueError: If the destination file is not in the correct format.
        
        Requires:
            The source file must be in the correct format. Each word must be on a separate line. Words must contain only alphabetic characters.
            The destination file must be in the correct format. Each word must be on a separate line. Words must contain only alphabetic characters.
        """
        try:
            with open(source, "r") as f:
                source_words: List[str] = f.read().split("\n")
            with open(destination, "r") as f:
                destination_words: List[str] = f.read().split("\n")
            
            # Same validation as load_wordlist but optimized for this method
            source_words = list(set(source_words))
            destination_words = list(set(destination_words))

            # Remove leading and trailing whitespaces from each word
            source_words = [word.strip() for word in source_words]
            destination_words = [word.strip() for word in destination_words]

            if not all(word.isalpha() for word in source_words and not all(word.islower() for word in source_words)):
                raise ValueError("Invalid source file format. Words must be all-lowercase and contain only alphabetic characters.")

            if not all(word.isalpha() for word in destination_words and not all(word.islower() for word in destination_words)):
                raise ValueError("Invalid destination file format. Words must be all-lowercase and contain only alphabetic characters.")

            if any(len(word.split()) > 1 for word in source_words):
                raise ValueError("Invalid source file format. Each word must be on a separate line.")
            if any(len(word.split()) > 1 for word in destination_words):
                raise ValueError("Invalid destination file format. Each word must be on a separate line.")

            if not all(word.isalpha() for word in source_words):
                raise ValueError("Invalid source file format. Words must contain only alphabetic characters.")
            if not all(word.isalpha() for word in destination_words):
                raise ValueError("Invalid destination file format. Words must contain only alphabetic characters.")

            destination_words.extend(source_words)

            with open(destination, "w") as f:
                f.write("\n".join(destination_words))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error during stacking: {str(e)}")

    @staticmethod
    def merge_delete(source: str, destination: str) -> None:
        """
        Merges two wordlist files and deletes the words in the first file from the second file.

        Args:
            source (str): Path to the source file.
            destination (str): Path to the destination file.
        
        Returns:
            None
        
        Raises:
            FileNotFoundError: If the source file or destination file is not found.
            ValueError: If the source file is not in the correct format.
            ValueError: If the destination file is not in the correct format.
        
        Requires:
            The source file must be in the correct format. Each word must be on a separate line. Words must contain only alphabetic characters.
            The destination file must be in the correct format. Each word must be on a separate line. Words must contain only alphabetic characters.
        """
        try:
            with open(source, "r") as f:
                source_words: List[str] = f.read().split("\n")
            with open(destination, "r") as f:
                destination_words: List[str] = f.read().split("\n")

            if any(len(word.split()) > 1 for word in source_words):
                raise ValueError("Invalid source file format. Each word must be on a separate line.")
            if any(len(word.split()) > 1 for word in destination_words):
                raise ValueError("Invalid destination file format. Each word must be on a separate line.")

            if not all(word.isalpha() for word in source_words):
                raise ValueError("Invalid source file format. Words must contain only alphabetic characters.")
            if not all(word.isalpha() for word in destination_words):
                raise ValueError("Invalid destination file format. Words must contain only alphabetic characters.")
            
            # Same validation as load_wordlist but optimized for this method

            # Remove leading and trailing whitespaces from each word
            source_words = [word.strip() for word in source_words]

            # Remove leading and trailing whitespaces from each word
            destination_words = [word.strip() for word in destination_words]

            source_words = list(set(source_words))
            destination_words = list(set(destination_words))

            if not all(word.isalpha() for word in source_words and not all(word.islower() for word in source_words)):
                raise ValueError("Invalid source file format. Words must be all-lowercase and contain only alphabetic characters.")

            if not all(word.isalpha() for word in destination_words and not all(word.islower() for word in destination_words)):
                raise ValueError("Invalid destination file format. Words must be all-lowercase and contain only alphabetic characters.")
            

            destination_words_ = list(set(destination_words) - set(source_words))

            # All other words in the source file that are not in the destination file will be added to the destination file

            destination_words_ += [word for word in source_words if word not in destination_words]

            with open(destination, "w") as f:
                f.write("\n".join(destination_words_))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error during merge delete: {str(e)}")
    
    def clear_cache(self, cache_file: str = "lesp_cache/lesp.cache") -> None:
        """
        Clears the cache file.

        Args:
            cache_file (str): Path to the cache file.
        
        Returns:
            None

        Raises:
            FileNotFoundError: If the cache file is not found.
            ValueError: If the cache file is not specified.
        
        Requires:
            The cache file must be in the correct format. Each word must be on a separate line. Words must contain only alphabetic characters.
        """
        if cache_file:
            try:
                os.remove(cache_file)
                self.cache = {}
                # If there also was a directory, remove it
                if os.path.isdir(os.path.dirname(cache_file)):
                    os.rmdir(os.path.dirname(cache_file))
            except FileNotFoundError:
                raise FileNotFoundError(f"{cache_file} not found!")
        else:
            raise ValueError("Cache file not specified!")
    

