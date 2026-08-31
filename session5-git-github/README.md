# Git Homework - Commit Flags & Cherry-Pick

## Task 1: git commit -a -m vs git commit -m

`git commit -m "message"` only commits changes that are already staged with `git add` but if a tracked file is modified but not staged, it's doesn't do anything.

`git commit -a -m "message"` automatically stages all modified **tracked** files before committing, so you skip the `git add` step.You can say it merges git add and git commit kind of but  it does not stage new/untracked files , those still need `git add` first.  

### Modified a tracked file, then tried git commit -m without staging

```
$ git commit -m "try commit without staging"
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   notes.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

Nothing got committed because the change was never staged.

### Same modified file, now using git commit -a -m

```
$ git commit -a -m "added line 2 to notes"
[master 05c29ec] added line 2 to notes
 1 file changed, 1 insertion(+)
```

This time it committed directly, because `-a` auto-staged the modified tracked file.

### Proof that -a does not work on new files

```
$ git status
?? extra.txt

$ git commit -a -m "try committing new file with -a"
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	extra.txt

nothing added to commit but untracked files present (use "git add" to track)
```

`extra.txt` is a new file, so `git status` marks it `??` (untracked). Even `-a` skipped it. That confirms `-a` only auto-stages files git is already tracking.

## Task 2: Git Cherry-Pick

### Step 1: 2-4 commits on main branch

```
$ git log --oneline
eeb583b add feature C
2e707af add feature B
8453f3c add feature A
05c29ec added line 2 to notes
ec168ee initial commit
```

### Step 2: New branch with 2-3 commits

```
$ git checkout -b feature-branch
Switched to a new branch 'feature-branch'

$ git log --oneline
e4a46ce add logout button
47965e9 add signup page
5da2507 add login page
eeb583b add feature C
2e707af add feature B
8453f3c add feature A
05c29ec added line 2 to notes
ec168ee initial commit
```

### Step 3: Cherry-pick one commit from feature-branch into main

Picked commit (add signup page) from `feature-branch` into `master`.
We have to use the hash_id for cherrypick.

```
$ git checkout master
Switched to branch 'master'

$ git cherry-pick 47965e9
[master 85bb867] add signup page
 Date: Mon Aug 31 23:22:28 2026 +0530
 1 file changed, 1 insertion(+)
 create mode 100644 signup.txt
```

### Step 4: Verify the change is now on main

```
$ git log --oneline
85bb867 add signup page
eeb583b add feature C
2e707af add feature B
8453f3c add feature A
05c29ec added line 2 to notes
ec168ee initial commit

$ ls
notes.txt
signup.txt

$ cat signup.txt
signup page added
```

`signup.txt` now exists on `master` even though it was originally created on `feature-branch`. Only the `add signup page` commit was picked. `add login page` and `add logout button` are still only on `feature-branch`, which confirms cherry-pick copies just the one chosen commit, not the whole branch.
