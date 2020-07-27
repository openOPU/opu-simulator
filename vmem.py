import numpy as np

MEM_SIZE = 1 << 32
PAGE_SIZE = 1024 * 1024
PAGE_COUNT = MEM_SIZE // PAGE_SIZE

class VirtualMemory:
    """This class simulates a memory devive."""

    def __init__(self):
        """Initialize the empty memory."""

        self.pages = [None] * PAGE_COUNT

    @staticmethod
    def newpage():
        """Return a fresh unitialized page."""

        return np.empty(PAGE_SIZE, dtype=np.uint8)

    def __getitem__(self, i):
        """Return the values stored in memory."""

        if isinstance(i, slice):
            first_page = i.start // PAGE_SIZE
            offset_of_first = i.start % PAGE_SIZE
            last_page = (i.stop - 1) // PAGE_SIZE
            offset_of_last = (i.stop - 1) % PAGE_SIZE
            pages = self.pages[first_page:last_page+1]
            if any(x is None for x in pages):
                raise RuntimeError('Page fault! -- Failed read at address 0x%x' % i.start)
            if len(pages) == 1:
                pages[0] = pages[0][offset_of_first:offset_of_last+1]
            else:
                pages[0] = pages[0][offset_of_first:]
                pages[-1] = pages[-1][:offset_of_last+1]
            data = np.concatenate(pages)
            return data[::i.step]

        if isinstance(i, int):
            page_idx = i // PAGE_SIZE
            offset_in_page = i % PAGE_SIZE
            if self.pages[page_idx] is None:
                raise RuntimeError('Page fault! -- Failed read at address 0x%x' % i)
            return self.pages[page_idx][offset_in_page]

        raise ValueError('Invalid argument')

    def __setitem__(self, i, value):
        """Write values into memory."""

        if isinstance(i, slice):
            step = i.step
            if step is None:
                step = 1
            first_page = i.start // PAGE_SIZE
            offset_of_first = i.start % PAGE_SIZE
            last_page = (i.stop - 1) // PAGE_SIZE
            value_idx = 0
            for k in range(first_page, last_page + 1):
                if self.pages[k] is None:
                    self.pages[k] = self.newpage()
                page = self.pages[k]
                count = page[offset_of_first::step].size
                count = min(count, value.size - value_idx)
                offset_of_last = offset_of_first + count * step
                page[offset_of_first:offset_of_last:step] = value[value_idx:value_idx+count]
                value_idx += count
                offset_of_first += step * count
                offset_of_first %= PAGE_SIZE
            if value_idx != value.size:
                raise RuntimeError('Invalid write!')

        elif isinstance(i, int):
            page_idx = i // PAGE_SIZE
            offset_in_page = i % PAGE_SIZE
            if self.pages[page_idx] is None:
                self.pages[page_idx] = self.newpage()
            self.pages[page_idx][offset_in_page] = value

        else:
            raise ValueError('Invalid argument')
