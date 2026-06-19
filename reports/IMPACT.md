# IMPACT.md — what breaks if we change X

**Changed component:** `tqdm`

## Blast radius — 135 dependent caller(s) (reverse-reachable)

- test_exceptions()
- test_main()
- test_manpath()
- Test warning info in     `pandas.Dataframe(Series).progress_apply(func, *args)`
- Test bar object instance as argument deprecation
- test_pandas_apply_args_deprecation()
- test_pandas_deprecation()
- Test overhead of manual tqdm
- Test overhead of manual tqdm (hard)
- Test overhead of manual tqdm vs simple progress bar (hard)
- test_iter_overhead()
- test_iter_overhead_hard()
- test_iter_overhead_simplebar_hard()
- test_manual_overhead()
- test_manual_overhead_hard()
- test_manual_overhead_simplebar_hard()
- incr_bar()
- Test on multiple bars, one not needing miniters adjustment
- Test multiprocessing.Pool
- Test concurrent.futures.ThreadPoolExecutor
- Test for stalled tqdm instance and monitor deletion
- test_imap()
- test_monitoring_and_cleanup()
- test_monitoring_multi()
- test_threadpool()
- Test exponential weighted average smoothing
- Test nested progress bars
- Test custom bar formatting
- Test resetting a bar for re-use
- Test positioned progress bars
- Test internal GUI properties
- Test comparison functions
- Test clearing bar display
- Test refresh bar display
- Test advance len (numpy array shape)
- Test autodisable will disable on non-TTY
- Test directly assigning non-str objects to postfix
- Test numeric `unit_scale`
- Native strings written to unspecified files
- Unicode strings written to specified files
- Test write_bytes argument with and without `file`
- Test output to arbitrary file-like objects
- Test `leave=True` always prints info about the last iteration
- Test purely dynamic miniters (and manual updates and __del__)
- Test large mininterval
- Test smoothed dynamic miniters
- Test smoothed dynamic miniters with mininterval
- Check that the RLock has not been constructed.
- Test treatment of infinite total
- Test unknown total length
- Test ascii/unicode bar
- Test manual creation and updates
- Test manual creation and closure and n_instances
- _rlock_creation_target()
- test_all_defaults()
- test_ascii()
- test_autodisable_disable()
- test_autodisable_enable()
- test_bar_format()
- test_big_min_interval()
- test_clear()
- test_clear_disabled()
- test_close()
- test_cmp()
- test_deprecated_gui()
- test_deprecated_nested()
- test_disable()
- test_disabled_refresh()
- test_dynamic_min_iters()
- test_external_write()
- test_file_output()
- test_file_redirection()
- test_float_progress()
- test_infinite_total()
- test_iterate_over_csv_rows()
- test_leave_option()
- test_len()
- test_max_interval()
- test_min_interval()
- test_min_iters()
- test_native_string_io_for_default_file()
- test_nototal()
- test_position()
- test_postfix()
- test_postfix_direct()
- test_refresh()
- test_repr()
- test_reset()
- test_set_description()
- test_smoothed_dynamic_min_iters()
- test_smoothed_dynamic_min_iters_with_min_interval()
- test_smoothing()
- test_trange()
- test_unicode_string_io_for_specified_file()
- test_unit()
- test_unit_scale()
- test_unpause()
- test_update()
- test_write()
- test_write_bytes()
- main()
- Parameters (internal use only)     ---------     fp  : file-like object for tqdm
- # TODO: add custom support for some of the following?
- GUI progressbar decorator for iterators. Includes a default (x)range iterator pr
- Experimental GUI version of tqdm!
- # TODO: @classmethod: write() on GUI?
- # TODO: somehow allow the following:
- tgrange()
- tqdm_gui
- IPython/Jupyter Notebook progressbar decorator for iterators. Includes a default
- Experimental IPython/Jupyter Notebook widget using tqdm!
- tnrange()
- tqdm_notebook
- Customisable progressbar decorator for iterators. Includes a default (x)range it
- # TODO: private method
- A shortcut for tqdm(xrange(*args), **kwargs).     On Python3+ range is used inst
- Decorate an iterable object, returning an iterator which acts exactly     like t
- # TODO: check this doesn't overwrite another fixed bar
- trange()
- auto.py
- autonotebook.py
- cli.py
- gui.py
- __init__.py
- __main__.py
- notebook.py
- std.py
- tests_pandas.py
- tests_perf.py
- tests_synchronisation.py
- tests_tqdm.py
- _tqdm_gui.py
- _tqdm_notebook.py
- _tqdm.py
- _utils.py

## God-Node betweenness — the Bridges most affected by change

| Bridge | Betweenness |
| --- | ---: |
| tqdm | 0.5066 |
| closing() | 0.1512 |
| tests_tqdm.py | 0.1219 |
| StringIO | 0.1149 |
| std.py | 0.108 |
