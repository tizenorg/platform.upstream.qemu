#!/bin/bash -e
#
# While updating versions of QEMU to 1.0 I got fed up with the
# quilt workflow and just put up a git tree that contains all
# the commits on top of a stable tarball.
#
# When updating this package, just either update the git tree
# below (use rebase!) or change the tree path and use your own
#
# That way we can easily rebase against the next stable release
# when it comes.

GIT_TREE=git://github.com/openSUSE/qemu.git
GIT_LOCAL_TREE=~/git/qemu-opensuse
GIT_BRANCH=opensuse-2.0
GIT_UPSTREAM_TAG=v2.0.0
QEMU_TMP=/dev/shm/qemu-tmp

restore_file_to_package() {
# If the processed file matches the previous one, move the previous
# one back in place, otherwise add the processed file.

    if cmp -s "$1" saved."$1"; then
        osc mv --force saved."$1" "$1"
    else
        osc add "$1"
    fi
}

# save files in case they remain unchanged
if [ -e 0001-* ]; then
    for i in 0*; do
        osc mv $i saved.$i
    done
fi
osc mv qemu.spec saved.qemu.spec
osc mv qemu-linux-user.spec saved.qemu-linux-user.spec

# fetch all patches
rm -rf $QEMU_TMP
OSCDIR="$(pwd)"
if [ -d "$GIT_LOCAL_TREE" ]; then
    git clone -ls $GIT_LOCAL_TREE $QEMU_TMP
    cd $QEMU_TMP
else
    git clone $GIT_TREE $QEMU_TMP
    cd $QEMU_TMP
    git remote add upstream git://git.qemu.org/qemu.git
    git remote update
fi
git checkout $GIT_BRANCH 
git format-patch -N $GIT_UPSTREAM_TAG -o "$OSCDIR"
QEMU_VERSION=`cat VERSION`
cd "$OSCDIR"
rm -rf $QEMU_TMP

# cut off file name after 40 bytes, so we work around git version differences
# while at it, also remove the signature.
for i in 0*; do
    PATCHNAME=${i%.patch}
    PATCHNAME=${PATCHNAME:0:40}.patch
    head -n $(expr $(wc -l $i | cut -d ' ' -f 1) - 3) $i > "$PATCHNAME.tmp"
    rm "$i"
    mv "$PATCHNAME.tmp" "$PATCHNAME"
    restore_file_to_package "$PATCHNAME"
done

# we have all patches as files now - generate the spec files!
for package in qemu qemu-linux-user; do
  while IFS= read -r line; do
    if [ "$line" = "PATCH_FILES" ]; then
        for i in 0*; do
            NUM=${i%%-*}
            echo -e "Patch$NUM:      $i"
        done
    elif [ "$line" = "PATCH_EXEC" ]; then
        for i in 0*; do
            NUM=${i%%-*}
            echo "%patch$NUM -p1"
        done
    elif [ "$line" = "QEMU_VERSION" ]; then
        echo "Version:        $QEMU_VERSION"
    elif [[ "$line" =~ ^Source: ]]; then
        QEMU_TARBALL=qemu-`echo "$line" | cut -d '-' -f 2-`
        VERSION_FILE=${QEMU_TARBALL%.tar.bz2}/roms/seabios/.version
        SEABIOS_VERSION=`tar jxfO "$QEMU_TARBALL" "$VERSION_FILE"`
        SEABIOS_VERSION=`echo $SEABIOS_VERSION | cut -d '-' -f 2`
        echo "$line"
    elif [ "$line" = "SEABIOS_VERSION" ]; then
        echo "Version:        $SEABIOS_VERSION"
    else
        echo "$line"
    fi
  done < $package.spec.in > $package.spec
done

restore_file_to_package qemu.spec
restore_file_to_package qemu-linux-user.spec

# remove any remaining saved files
files=(saved.*)
if [ -e "${files[0]}" ]; then
    osc rm --force saved.*
fi

