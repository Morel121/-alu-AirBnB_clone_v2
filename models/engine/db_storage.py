def close(self):
        """Calls remove() method on private session attribute or close() on Session."""
        self.__session.remove()
