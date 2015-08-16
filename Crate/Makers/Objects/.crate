
import Core.Maker
import Core.FS
import Core.Action
import Core.Types

class ObjectMaker(Core.Maker.Maker):
    source_suffix = '.c'
    target_suffix = '.o'
    def sources(self, config):
        glob_string = "*%s" % self.source_suffix
        return core.fs.glob(config=config, pattern=glob_string)

    def targets(self, config, sources):
        return core.types.List([s.target_node(suffix=self.target_suffix) for s in sources])

    #todo: make function to check if a target is up to date

    def make(self, config, sources, targets):
        command_dict = core.types.Dict()
        command_dict.cc.update({
            'cc' : config.cc,
            'cc_flags' : config.cc_flags.prepare(),
            'include_flags' : config.include_flags.prepare(),
            'define_flags' : config.define_flags.prepare(),
            'environment_variables' : config.environment_variables.prepare(),
        )}
        
        command = [
            '$(environment_variables)s',
            '$(cc)s',
            '$(cc_flags)s',
            '$(define_flags)s',
            '$(target)s',
        ]
        command = ' '.join(command)

        tgts = Core.Types.List()

        for tgt in targets:
            command_dict.target = tgt
            command_line
            return_code = Core.Bash.run(command % command_dict, shell=True)
            if tgt.exists() is False:
                raise Core.Error.MakerError('Failed make object: %s' % tgt)
            
            tgt.up_to_date = True

            tgts.append(tgt)

        return tgts
