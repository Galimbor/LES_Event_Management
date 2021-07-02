/**
 * Receives json data from the server, converts it to a javascript object
 * renders the UI according to that data received
 * manipulates the data (create, read, update, delete)
 * sends it back to the server
 * @param {json}   jsonForm         Django form object in json.
 * @param {json}   tiposCampo    Django campo types in json
 * @param {string}   containerDivId Id of the div where the form will be rendered
*/

const ESCOLHA_MULTIPLA = 12; //Primary Key na base de dados de uma pergunta de escolha multipla
var NEW_CAMPO_COUNTER = 0;
var FormManager = class {

    /** CONSTRUCT OBJECT Updated**/
    constructor(formularioJson, tipo_formulario, camposJson, subcamposJson, success_url, containerDivId = 'form-wrapper') {
        this.formulario = JSON.parse(formularioJson)[0];
        this.tipo_formulario = tipo_formulario
        this.campos = JSON.parse(camposJson);
        this.subcampos = JSON.parse(subcamposJson);
        this.container = $('#' + containerDivId);
        this.activeCampo = null;
        this.success_url = success_url;
        
        let form = this;
        // collapse campos when clicking outside
        $(window).click(e => form.colapseCampos($('.campos-item')));

        $('.button.publish').click(function(){

            let selected_option = document.querySelector('input[name="answer"]:checked').dataset.id;
            // console.log( $('input[name="answer"]:checked').data('id'))
            console.log(selected_option)
            form.publishForm(selected_option) //this is a HTML element   
        })

        $('.button.save-form').click(e => form.saveRemotely())


    }


    /** RENDER OBJECT **/
    /*
    * Parses json object received from the server to javascrit
    * @param {JSON} rawForm Json form data.
    * @return {object} javascript form object.
    */
    parseJsonForm(rawForm) {
        //The UI already has support for secctions 
        //in case we want to implement them
        var formObj = {
            id: 'form-1',
            title: '',
            description: '',
            campos: []
        }
        formObj.campos = JSON.parse(rawForm);
        return formObj
    }

    /* colapse html campos*/
    colapseCampos(items) {
        items.find('.card-header, .campos-config').addClass('is-hidden');
        items.find('input, textarea').not('[disabled]').addClass('is-static');
        items.removeClass('campos-item-active')
    }

    /* expand html campos*/
    expandCampos(questionItems) {
        questionItems.find('.card-header, .campos-config').removeClass('is-hidden');
        questionItems.find('input, textarea').not('[disabled]').removeClass('is-static');
        questionItems.addClass('campos-item-active')
    }

    /*
    * Shows html campo element as active and updates activeCampo variable
    * @param {JQuery Object} campoHtml
    * Note: works on jquery object (campoHtml) only. To activate campo 
    * using a campoObj we have to set form.activeCampo = campoObj
    */
    activateCampo(campoHtml) {
        let todosCampos = $('.campos-item');
        this.colapseCampos(todosCampos);
        this.expandCampos(campoHtml)
        this.activeCampo = form.getCampoById(campoHtml.data('id'));
        let padding = $('#subnavbar').height()+20
        $('html, body').animate({
            scrollTop: campoHtml.offset().top-padding 
        });
    }


    setHtmlData(obj, htmlDiv) {

        for (var key in obj.fields) {
            var value = obj.fields[key];
            var objName = obj.model.split('.')[1]
            htmlDiv.find(`.${objName}__${key}`).each(function(){
                var element = $(this);
                if (element.is(':checkbox'))
                    element.prop( "checked", value );
                else if (element.is('input'))
                    element.val(value);
                else if (key == 'position_index')
                    element.html(value + 1);
                else element.html(value);

            })
            
        }
    }

    /*
    * Obtem o template HTML do tipo de campo
    * @param {int} tipoCampoId
    */
    getTipoCampoHtmlTemplate(tipoCampoId){
        var result;
        var tiposCamposHtml = $('.campos-template-wrap').find('.campo-template')
        tiposCamposHtml.each(
            (i, tipocampo ) => ($(tipocampo).data('id') == tipoCampoId) ? result = $(tipocampo) : null
        )
        return result.clone()
    }

    /*
    * Obtem o HTML de um determinado campo
    * @param {int} campoId
    */
    getCampoHtml(campoId){
        return $(`.campos-item[data-id=${campoId}]`).not('[data-campo-relacionado]')
    }

    setCampoEventListeners(campoHtml){
        var form = this;
    
        campoHtml.find('.campos-delete-btn').click(function (e) {
            e.stopPropagation();
            form.deleteCampo($(this).data('id'), $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campos-move-up').click(function (e) {
            e.stopPropagation();
            form.moveCampo($(this).data('id'), -1, $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campos-create').click(function (e) {
            e.stopPropagation();
            form.createCampo(ESCOLHA_MULTIPLA, $(this).data('campo-relacionado')); 
        })
        campoHtml.find('.campos-move-down').click(function (e) {
            e.stopPropagation();
            form.moveCampo($(this).data('id'), 1, $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campo__conteudo').change(function () {
            form.updateCampo($(this).data('id'), $(this).val(), $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campo__obrigatorio').change(function () {
            var campo = form.getCampoById($(this).data('id'));
            campo.fields.obrigatorio = $(this).is(':checked');
        })
        campoHtml.not('[data-campo-relacionado]').click(function (e) {
            e.stopPropagation();
            form.activateCampo($(this));
        })
    }

    /*
    * Creates a html element for a campo
    * @param {object} campo
    */
    createCampoHtml(campoObj, isSubcampo=false) {
        var form = this;
        //create element

        var baseTemplateId = isSubcampo? '#subcampo-template-base': '#campo-template-base';
        var campoHtml = $(baseTemplateId).clone();
        campoHtml.find('.campo-content').html(
            this.getTipoCampoHtmlTemplate(campoObj.fields.tipocampoid)
        );
        
        //pass data id for action buttons and input fields
        campoHtml.find('a, button, input').addBack().attr(
            'data-id',
            campoObj.pk);
        //pass data id for action buttons and input fields
        campoHtml.removeClass('is-hidden');
        campoHtml.attr('id','campo'+campoObj.pk)

        
        if(isSubcampo){
            campoHtml.find('a, button, input').addBack()
                .attr('data-campo-relacionado',campoObj.fields.campo_relacionado)
                .attr('data-tipocampoid',campoObj.fields.tipocampoid)
                .addClass('is-small');
            campoHtml.find('.subcampos').removeClass('subcampos')
        }

        //fill data
        this.setHtmlData(campoObj, campoHtml);
        //if (campoObj == this.activeCampo)
        //    this.activateCampo(campoHtml);
        
        this.setCampoEventListeners(campoHtml);

        return campoHtml;
    }

    /*
    * Renders a campo in the form and updates its position when this parameter is passed
    * @param {string} id of the form.
    * @param {object} campo object.
    * @param {int} (optional) campo index position in the list of campos.
    */
    renderCampo(formDivId, campoObj, campoPosicao = null) {
        //update positions
        var form = this;
        if (campoPosicao >= 0)
            campoObj.fields.position_index = campoPosicao;

        var campoHtml = form.createCampoHtml(campoObj);
        var camposContainer = this.container.find(`#${formDivId} .campos`);

        //render subcampos
        var subCamposCount=0;
        self.form.subcampos.forEach(function(subcampo){
            if(!subcampo.delete)
                if(subcampo.fields.campo_relacionado==campoObj.pk){
                    if(!subCamposCount)
                        campoHtml.find('.subcampos').html('');
                    subcampo.fields.position_index = campoPosicao+(subCamposCount+1)/10;
                    var subCampoHtml = form.createCampoHtml(subcampo, true);
                    campoHtml.find('.subcampos').append(subCampoHtml);
                    subCamposCount++;
                }
        })

        camposContainer.append(campoHtml);
    }

    //Updated
    renderFormulario(){
        var formDiv = $('#form-template').clone();
        this.container.append(formDiv);
        formDiv.removeClass('is-hidden');
        formDiv.attr('id', 'form-1');
        this.setHtmlData(this.formulario, $('#gestor-templates-wrapper'))  
        var form = this; 

        //listeners 
        $('.form-header').click(function (e) {
            e.stopPropagation();
            form.expandCampos($(this));
        })
        formDiv.find('.formulario__nome').change(function (e) {
            form.formulario.fields.nome = $(this).val()
            $('.formulario__nome').html($(this).val());
        })

        //*********************** */
        // ***** SETTINGS *******
        // ***********************
        let tipo_formulario_before = this.formulario.fields.tipoformularioid
        let istemplate_before = this.formulario.fields.is_template;
        let tipo_evento_before = this.formulario.fields.tipoeventoid;
        
        
        function selectEventType(){
            let tipo_form = $('.tipo_formulario option:selected').data("tipoformulario")
            if (tipo_form == 3){ //bad practice, must check later, ID can change
                $('.tipo-evento-options').removeClass('is-hidden')
                $('.tipo_evento_formulario option').each(function()
                {
                    if($(this).data("tipo-evento") == tipo_evento_before )
                        $(this).attr("selected" , "selected")                
                })
            }
            else
                $('.tipo-evento-options').addClass('is-hidden')
        }
        $('.escolher_tipo_formulario').change(
            selectEventType
        )

        $('.button.ver_form_config').click(e => {
            
            $('.modal.ver_form_config').addClass('is-active')
            // Tipo de Formulario, Funcao que serve para selecionar qual foi o tipo selecionado anteriormente
            $('.tipo_formulario option').removeAttr("selected")
            $('.tipo_formulario option').each(function()
            {
                if($(this).data("tipoformulario") == tipo_formulario_before )
                    $(this).attr("selected" , "selected")                
            })
           
            selectEventType()

            //Tornar template
            $('.is_template_option input').prop("checked", false)
            $('.is_template_option input').each(function(){
                if($(this).data("id") == istemplate_before)
                    $(this).prop("checked" , true)      
            })       
        })

        // SAVE SETTINGS
        $('.button.save-form-settings').click(e => {

            // Tipo de Formulario
            form.formulario.fields.tipoformularioid = $('.tipo_formulario option:selected').data("tipoformulario")
            


            // Tipo de Evento
            if (form.formulario.fields.tipoformularioid == 3){
                form.formulario.fields.tipoeventoid = $('.tipo-evento-options option:selected').data("tipo-evento")
            }
            //Tornar template
            form.formulario.fields.is_template= $('.is_template_option input:checked').data("id") 
            
            this.saveRemotely();

            $('.ver_form_config').removeClass('is-active')

        })


        // ********************************
        // *********** PUBLISH
        // *******************************
        $('.button.ver_form_publish').click(e => $('.modal.ver_form_publish').addClass('is-active'))

        // *********** FIELDS
        $('.create-campo-from-tipo').click(function (e) {
            e.stopPropagation();
            form.createCampo($(this).data('id'), $(this).data('campo-relacionado'));
        })


    }

    /*
    * Renders the entire form
    */
    renderAll() {
        //render form
        this.container.html('');
        this.renderFormulario()
        //render campos
        let campos = this.campos.filter(obj => !obj.hasOwnProperty('delete')? obj: null)
        campos.forEach((c, i) => !c.delete? this.renderCampo('form-1', c, i): null);
        if(this.activeCampo)
            this.activateCampo(this.getCampoHtml(this.activeCampo.pk))
    }

    /** MANIPULATE OBJECT **/

    isSubcampo(campoObj){
        return (campoObj && campoObj.fields.campo_relacionado!=null)? true : false;
    }
    
    /*
    * Selects a campo by id
    * @param {int} campo id/pk .
    */
    getCampoById(questionId, listaCampos=null) {
        var result;
        var campos = listaCampos? listaCampos: this.campos;
        campos.some(function (q,i) {
            if (q.pk == questionId) {
                result = q;
                result.array_index = i;
                return true;
            }
        });
        return result;
    }

    /*
    * Reorders the position of campos and rerenders the form
    * @param {int} campo id/pk to be repositioned.
    */
    moveCampo(campoID, moveCount, campoRelacionado=null) {
        var campos, campoObj;
        var boundStart, boundEnd;
        if (campoRelacionado){
            campoObj = form.getCampoById(campoID, this.subcampos)
            campos = this.subcampos;
            boundStart=0, boundEnd=campos.length;
        }
        else{
            campoObj = form.getCampoById(campoID, this.campos)
            campos = this.campos
            boundStart=0, boundEnd=campos.length;
        }
        var oldPosition = campoObj.array_index;
        var newPosition = oldPosition + moveCount;
        if (newPosition >= boundStart && newPosition < boundEnd) {
            //remove from old position
            campos.splice(oldPosition, 1);
            //insert at new position
            campos.splice(newPosition, 0, campoObj);
            this.renderAll();
        }
    }

    /*
    * Creates a campo
    * @param {int} campo type pk.
    */
    createCampo(tipocampo, campoRelacionado=null) {
        var campos;
        if (campoRelacionado){

            campos = this.subcampos;
        }
        else{
            campos = this.campos
        }
        // TODO it should request the server to create a campo
        // this way it will always be in sync with the database
        var campoObj = {
            "model": "forms_manager.campo",
            "pk":  --NEW_CAMPO_COUNTER,
            "fields": {
                "conteudo": "",
                "tipocampoid": tipocampo,
                "position_index": 0,
                "campo_relacionado": campoRelacionado,
                "obrigatorio": false,
                "respostapossivelid": null
            }
        }

        if(tipocampo==ESCOLHA_MULTIPLA && campoRelacionado==null )
            this.createCampo(ESCOLHA_MULTIPLA, campoObj.pk);
        if(campoRelacionado==null)
            this.activeCampo = campoObj

        campos.push(campoObj);
        this.renderAll();
    }


    /*
    * Creates a campo
    * @param {int} campo id/pk.
    * @param {int} campo id/pk.
    */
    updateCampo(campoID, val, campoRelacionado) {
        var campos, campoObj;
        if (campoRelacionado){
            campoObj = form.getCampoById(campoID, this.subcampos)
            campos = this.subcampos;
        }
        else{
            campoObj = form.getCampoById(campoID, this.campos)
            campos = this.campos
        }
        campoObj.fields.conteudo = val;
    }

    /*
    * Deletes a campo
    * @param {int} campo id/pk.
    */
    deleteCampo(campoID, campoRelacionado=null) {
        let campos, campoObj;
        let isParent = (campoRelacionado==null);
        this.activeCampo = null; 
        if (isParent){
            campoObj = form.getCampoById(campoID, this.campos)
            campos = this.campos
        }
        else{
            campoObj = form.getCampoById(campoID, this.subcampos)
            campos = this.subcampos;
        }
        // if not saved in db yet, deletes normally
        if (campoObj && campoObj.pk < 0) {
            campos.splice(campoObj.array_index, 1);
            
            //delete subcampos
            
            if (isParent){
                let camposRelacionados = this.subcampos.filter(
                    e => e.fields.campo_relacionado==campoID
                ) 
                let form = this;
                camposRelacionados.forEach(function(element){
                    let index = form.subcampos.indexOf(element);
                    form.subcampos.splice(index, 1)
                })
            }
            this.renderAll();
        }
        // else, marks for deletion
        else {
            campoObj.delete=true
            this.renderAll();
        }
    }

    toggleSubCampos(toggleButton){
        let campos = $('.campos-item');
        if (campos.hasClass('campos-item-collapsed')){
            toggleButton.find('.fas, svg').removeClass('fa-expand').addClass('fa-compress')
            campos.removeClass('campos-item-collapsed')
        }
        else{
            toggleButton.find('.fas, svg').removeClass('fa-compress').addClass('fa-expand')
            campos.addClass('campos-item-collapsed')
        }    
    }

    /***
     * Publish form
     */
    publishForm(id){
        if(id){
            this.formulario.fields.visibilidade = id;
            this.saveRemotely();
            
        }
        else {
            // this doesnt work #TODO
            // alert("Deve selecionar pelo menos uma opção!");
        }
    }


    formValid(){
        return $('#form').parsley().validate()
    }

    /*
    * Posts form
    */
    saveRemotely() 
    {
        if(this.formValid())
        {
        let success_url = this.success_url
        $.ajax({
            contentType: 'application/json; charset=utf-8',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: JSON.stringify(this),
            dataType: 'json',
            

            success: function(response) {
                if(response.status == 'ok'){
                    location.replace(success_url);
                }
            },
            error: function(response) {
                console.log(response);
                //informar utilizador que nao foi possível guardar no servidor, e a respectiva razão
                //guardar localmente ?
            }
        })
    }
}
};