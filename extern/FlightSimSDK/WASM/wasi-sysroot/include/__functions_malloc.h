#ifndef __wasilibc___functions_malloc_h
#define __wasilibc___functions_malloc_h

#define __need_size_t
#define __need_wchar_t
#define __need_NULL
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

void *malloc(size_t __size) __attribute__((__malloc__, __warn_unused_result__));
void free(void *__ptr);
void *calloc(size_t __nmemb, size_t __size) __attribute__((__malloc__, __warn_unused_result__));
void *realloc(void *__ptr, size_t __size) __attribute__((__warn_unused_result__));

//ASOBO MOD : esoria
struct mallinfo {
  unsigned int arena;    /* non-mmapped space allocated from system */
  unsigned int ordblks;  /* number of free chunks */
  unsigned int smblks;   /* always 0 */
  unsigned int hblks;    /* always 0 */
  unsigned int hblkhd;   /* space in mmapped regions */
  unsigned int usmblks;  /* maximum total allocated space */
  unsigned int fsmblks;  /* always 0 */
  unsigned int uordblks; /* total allocated space */
  unsigned int fordblks; /* total free space */
  unsigned int keepcost; /* releasable (via malloc_trim) space */
};
#define STRUCT_MALLINFO_DECLARED 1

void mallinfo(struct mallinfo* outRes);

int malloc_trim(size_t pad);

struct mchunkit {
  unsigned int curseg;
  unsigned int curchk;
  unsigned int chksz;
  unsigned int inuse;
};
#define STRUCT_MCHUNKIT_DECLARED 1

void mchunkit_begin(struct mchunkit* out);

void mchunkit_next(struct mchunkit* out);
//ASOBO END

#if defined(_GNU_SOURCE) || defined(_BSD_SOURCE)
void *reallocarray(void *__ptr, size_t __nmemb, size_t __size) __attribute__((__warn_unused_result__));
#endif

#ifdef __cplusplus
}
#endif

#endif
