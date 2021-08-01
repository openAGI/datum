<!-- markdownlint-disable -->

# API Overview

## Modules

- [`cache`](./cache.md#module-cache)
- [`cache.bucket`](./cache.bucket.md#module-cachebucket): To shuffle records (stable).
- [`configs`](./configs.md#module-configs)
- [`configs.config_base`](./configs.config_base.md#module-configsconfig_base)
- [`configs.default_configs`](./configs.default_configs.md#module-configsdefault_configs): Default write configs for TFRecord export.
- [`configs.tfr_configs`](./configs.tfr_configs.md#module-configstfr_configs)
- [`create_tfrecord`](./create_tfrecord.md#module-create_tfrecord)
- [`encoder`](./encoder.md#module-encoder)
- [`encoder.encoder`](./encoder.encoder.md#module-encoderencoder)
- [`encoder.tokenizer`](./encoder.tokenizer.md#module-encodertokenizer)
- [`export`](./export.md#module-export)
- [`export.export`](./export.export.md#module-exportexport)
- [`generator`](./generator.md#module-generator)
- [`generator.generator`](./generator.generator.md#module-generatorgenerator)
- [`generator.image`](./generator.image.md#module-generatorimage)
- [`generator.text`](./generator.text.md#module-generatortext)
- [`reader`](./reader.md#module-reader)
- [`reader.dataset`](./reader.dataset.md#module-readerdataset)
- [`reader.loader`](./reader.loader.md#module-readerloader)
- [`reader.parser`](./reader.parser.md#module-readerparser)
- [`reader.tfrecord_reader`](./reader.tfrecord_reader.md#module-readertfrecord_reader)
- [`serializer`](./serializer.md#module-serializer)
- [`serializer.serializer`](./serializer.serializer.md#module-serializerserializer)
- [`utils`](./utils.md#module-utils)
- [`utils.binary_utils`](./utils.binary_utils.md#module-utilsbinary_utils)
- [`utils.common_utils`](./utils.common_utils.md#module-utilscommon_utils)
- [`utils.hashing`](./utils.hashing.md#module-utilshashing): Stable hashing function using md5.
- [`utils.reader_utils`](./utils.reader_utils.md#module-utilsreader_utils)
- [`utils.shard_utils`](./utils.shard_utils.md#module-utilsshard_utils)
- [`utils.tqdm_utils`](./utils.tqdm_utils.md#module-utilstqdm_utils): Wrapper around tqdm.
- [`utils.types_utils`](./utils.types_utils.md#module-utilstypes_utils)
- [`version`](./version.md#module-version)
- [`writer`](./writer.md#module-writer)
- [`writer.tfrecord_writer`](./writer.tfrecord_writer.md#module-writertfrecord_writer)

## Classes

- [`bucket.DuplicatedKeysError`](./cache.bucket.md#class-duplicatedkeyserror)
- [`bucket.Shuffler`](./cache.bucket.md#class-shuffler): Stores data in temp buckets, restitute it shuffled.
- [`config_base.ConfigBase`](./configs.config_base.md#class-configbase): Base class for representing a set of tf.data config.
- [`tfr_configs.BucketConfigs`](./configs.tfr_configs.md#class-bucketconfigs): Bucket configuration used for bucketing sprase data into a batch.
- [`tfr_configs.DatasetConfigs`](./configs.tfr_configs.md#class-datasetconfigs): Dataset configuration.
- [`tfr_configs.TFRReadConfigs`](./configs.tfr_configs.md#class-tfrreadconfigs): TF Record Reader configuration.
- [`tfr_configs.TFRWriteConfigs`](./configs.tfr_configs.md#class-tfrwriteconfigs): TF Record writer configuration.
- [`encoder.Encoder`](./encoder.encoder.md#class-encoder): Feature Encoder abstract interface. Derived classes have to implement the encode method for
- [`encoder.GraphEncoder`](./encoder.encoder.md#class-graphencoder): Graph data encoder.
- [`encoder.ImageEncoder`](./encoder.encoder.md#class-imageencoder)
- [`encoder.NumberEncoder`](./encoder.encoder.md#class-numberencoder)
- [`encoder.StringEncoder`](./encoder.encoder.md#class-stringencoder): String encoder.
- [`tokenizer.BaseTokenizer`](./encoder.tokenizer.md#class-basetokenizer)
- [`tokenizer.InvertibleTokenizer`](./encoder.tokenizer.md#class-invertibletokenizer)
- [`generator.DatumGenerator`](./generator.generator.md#class-datumgenerator): Input data generator abstract interface. Derived classes have to implement geenrate_datum
- [`image.ClfDatumGenerator`](./generator.image.md#class-clfdatumgenerator): Image classification problem data generator.
- [`image.DetDatumGenerator`](./generator.image.md#class-detdatumgenerator): Image object Detection problem data generator.
- [`image.SegDatumGenerator`](./generator.image.md#class-segdatumgenerator): Generator for image Segmentation problem.
- [`text.TextJsonDatumGenerator`](./generator.text.md#class-textjsondatumgenerator): Text problem datum generator from json file.
- [`dataset.Dataset`](./reader.dataset.md#class-dataset): Public API to read tfrecord as tf.data.Dataset.
- [`parser.DatumParser`](./reader.parser.md#class-datumparser): TFRecord Example parser.
- [`tfrecord_reader.Reader`](./reader.tfrecord_reader.md#class-reader): Build a tf.data.Dataset object out of Instruction instance(s).
- [`serializer.DatumSerializer`](./serializer.serializer.md#class-datumserializer): Datum serializer. Encode data into serialized binary string.
- [`common_utils.AttrDict`](./utils.common_utils.md#class-attrdict): Enables acessing dict items as attributes.
- [`common_utils.memoized_property`](./utils.common_utils.md#class-memoized_property): Descriptor that mimics @property but caches output in member variable.
- [`hashing.Hasher`](./utils.hashing.md#class-hasher): Hasher: to initialize a md5 with salt.
- [`reader_utils.ReadInstruction`](./utils.reader_utils.md#class-readinstruction): Reading instruction for a dataset.
- [`tqdm_utils.EmptyTqdm`](./utils.tqdm_utils.md#class-emptytqdm): Dummy tqdm which doesn't do anything.
- [`tfrecord_writer.TFRecordWriter`](./writer.tfrecord_writer.md#class-tfrecordwriter): TFRecord writer interface.

## Functions

- [`bucket.get_bucket_number`](./cache.bucket.md#function-get_bucket_number): Returns bucket (shard) number (int) for given hashed key (int).
- [`config_base.create_config`](./configs.config_base.md#function-create_config): Creates a type-checked property.
- [`config_base.merge_configs`](./configs.config_base.md#function-merge_configs): Merges the given configs, returning the result as a new configs object.
- [`default_configs.get_default_write_configs`](./configs.default_configs.md#function-get_default_write_configs): Returns default write configs for a problem.
- [`create_tfrecord.main`](./create_tfrecord.md#function-main)
- [`encoder.datum_name_to_encoder`](./encoder.encoder.md#function-datum_name_to_encoder): Automatically identify encoder based on data values and problem type.
- [`export.export_to_tfrecord`](./export.export.md#function-export_to_tfrecord): Export data to tfrecord format.
- [`generator.deserialize`](./generator.md#function-deserialize): Deserializer for generator.
- [`loader.load`](./reader.loader.md#function-load): Load tfrecord dataset as `tf.data.Daatset`.
- [`tfrecord_reader.make_file_instructions`](./reader.tfrecord_reader.md#function-make_file_instructions): Returns instructions of the split dict.
- [`serializer.datum_to_tf_example`](./serializer.serializer.md#function-datum_to_tf_example): Builds tf.train.Example from (string -> int/float/str list) dictionary.
- [`serializer.serialize_datum`](./serializer.serializer.md#function-serialize_datum): Serialize the given example.
- [`binary_utils.is_binary_image`](./utils.binary_utils.md#function-is_binary_image): Determine image compression type using a binary string tensor/object.
- [`common_utils.add_metaclass`](./utils.common_utils.md#function-add_metaclass): Class decorator for creating a class with a metaclass.
- [`common_utils.check_and_image_shape`](./utils.common_utils.md#function-check_and_image_shape): Check whether a string is image filename.
- [`common_utils.datum_to_type_and_shape`](./utils.common_utils.md#function-datum_to_type_and_shape): Get object type and shape from value.
- [`common_utils.deserialize_object`](./utils.common_utils.md#function-deserialize_object): Deserialize object using name.
- [`common_utils.is_string`](./utils.common_utils.md#function-is_string): Check if the object contains string or bytes.
- [`common_utils.item_to_type_and_shape`](./utils.common_utils.md#function-item_to_type_and_shape): Datum item to type and shape.
- [`common_utils.load_module`](./utils.common_utils.md#function-load_module): Load python module using a given path; the path can be absolute or relative.
- [`common_utils.reraise`](./utils.common_utils.md#function-reraise): Reraise an exception with an additional message.
- [`common_utils.six_reraise`](./utils.common_utils.md#function-six_reraise)
- [`common_utils.try_reraise`](./utils.common_utils.md#function-try_reraise): Reraise an exception with an additional message.
- [`common_utils.zip_dict`](./utils.common_utils.md#function-zip_dict): Iterate over items of dictionaries grouped by their keys.
- [`shard_utils.get_read_instructions`](./utils.shard_utils.md#function-get_read_instructions): Returns a list of files (+skip/take) to read [from_:to] items from shards.
- [`shard_utils.get_shard_specs`](./utils.shard_utils.md#function-get_shard_specs): Returns list of _ShardSpec instances, corresponding to shards to write.
- [`shard_utils.raise_error_for_duplicated_keys`](./utils.shard_utils.md#function-raise_error_for_duplicated_keys): Log information about the examples and raise an AssertionError.
- [`shard_utils.write_tfrecord`](./utils.shard_utils.md#function-write_tfrecord): Write single (non sharded) TFrecord file from iterator.
- [`tqdm_utils.async_tqdm`](./utils.tqdm_utils.md#function-async_tqdm)
- [`tqdm_utils.disable_progress_bar`](./utils.tqdm_utils.md#function-disable_progress_bar): Disabled Tqdm progress bar.
- [`tqdm_utils.tqdm`](./utils.tqdm_utils.md#function-tqdm)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
